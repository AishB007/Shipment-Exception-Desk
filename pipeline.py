from chains import (
    classify_chain,
    escalate_chain,
    draft_email_chain
)

from tools import (
    calculate_delay_compensation,
    calculate_damage_compensation,
    calculate_loss_compensation
)


# --------------------------------------------------
# ESCALATION THRESHOLDS
# --------------------------------------------------

PREMIUM_THRESHOLD = 2000
STANDARD_THRESHOLD = 5000


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def process_exception(
    report: str,
    shipment_value: float,
    customer_tier: str
) -> dict:

    steps = []

    # --------------------------------------------------
    # STEP 1: VALIDATE INPUTS
    # --------------------------------------------------

    if not isinstance(report, str) or not report.strip():
        raise ValueError("The exception report cannot be empty.")

    if isinstance(shipment_value, bool):
        raise ValueError("Shipment value must be a valid number.")

    if not isinstance(shipment_value, (int, float)):
        raise ValueError("Shipment value must be numeric.")

    if shipment_value <= 0:
        raise ValueError("Shipment value must be greater than zero.")

    customer_tier = customer_tier.strip().lower()

    if customer_tier not in ("premium", "standard"):
        raise ValueError(
            "Customer tier must be premium or standard."
        )

    report = report.strip()

    steps.append("Input validated successfully.")

    # --------------------------------------------------
    # STEP 2: CLASSIFY THE REPORT
    # --------------------------------------------------

    classification = classify_chain.invoke({
        "report": report
    })

    category = classification.category.lower()

    steps.append(
        f"LLM classified the exception as '{category}'."
    )

    # --------------------------------------------------
    # STEP 3: CALCULATE COMPENSATION
    # --------------------------------------------------

    if category == "delayed":

        compensation_result = calculate_delay_compensation(
            shipment_value
        )

    elif category == "damaged":

        compensation_result = calculate_damage_compensation(
            shipment_value
        )

    elif category == "lost":

        compensation_result = calculate_loss_compensation(
            shipment_value
        )

    else:

        # Unknown reports receive no automatic compensation.
        compensation_result = {
            "category": "unknown",
            "shipment_value": round(shipment_value, 2),
            "compensation": 0.0,
            "currency": "INR",
            "policy": "Manual review required"
        }

    compensation = compensation_result["compensation"]

    steps.append(
        f"Compensation calculated: INR {compensation:.2f}."
    )

    # --------------------------------------------------
    # STEP 4: DETERMINE ESCALATION
    # --------------------------------------------------

    escalation_reason = None

    if category == "unknown":

        escalate = True
        escalation_reason = (
            "The report could not be reliably classified."
        )

    elif customer_tier == "premium" and (
        compensation > PREMIUM_THRESHOLD
    ):

        escalate = True
        escalation_reason = (
            f"Compensation exceeds the premium threshold "
            f"of INR {PREMIUM_THRESHOLD}."
        )

    elif customer_tier == "standard" and (
        compensation > STANDARD_THRESHOLD
    ):

        escalate = True
        escalation_reason = (
            f"Compensation exceeds the standard threshold "
            f"of INR {STANDARD_THRESHOLD}."
        )

    else:

        escalate = False

    steps.append(
        f"Escalation decision: "
        f"{'REQUIRED' if escalate else 'NOT REQUIRED'}."
    )

    if escalation_reason:
        steps.append(
            f"Escalation reason: {escalation_reason}"
        )

    # --------------------------------------------------
    # STEP 5: DRAFT THE APPROPRIATE MESSAGE
    # --------------------------------------------------

    common_inputs = {
        "report": report,
        "category": category,
        "shipment_value": f"INR {shipment_value:.2f}",
        "compensation": f"INR {compensation:.2f}",
        "customer_tier": customer_tier
    }

    if escalate:

        message_result = escalate_chain.invoke({
            **common_inputs,
            "escalation_reason": escalation_reason
        })

        message = message_result.content

        outcome = "Escalated for human review"

        steps.append(
            "Generated an internal escalation note for the manager."
        )

    else:

        message_result = draft_email_chain.invoke(
            common_inputs
        )

        message = message_result.content

        outcome = "Resolved automatically"

        steps.append(
            "Generated a customer-facing email."
        )

    # --------------------------------------------------
    # STEP 6: RETURN STRUCTURED RESULT
    # --------------------------------------------------

    return {
        "category": category,
        "shipment_value": round(shipment_value, 2),
        "customer_tier": customer_tier,
        "compensation": compensation,
        "currency": "INR",
        "escalated": escalate,
        "escalation_reason": escalation_reason,
        "outcome": outcome,
        "message": message,
        "steps": steps,
        "compensation_details": compensation_result
    }