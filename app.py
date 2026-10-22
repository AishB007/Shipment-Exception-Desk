import gradio as gr

from pipeline import process_exception
from session import triage_session


# --------------------------------------------------
# FORMAT DAILY LOG
# --------------------------------------------------

def format_log(records):

    if not records:
        return "No exceptions have been processed yet."

    lines = []

    for index, record in enumerate(records, start=1):

        lines.append(
            f"""
### Exception {index}

**Category:** {record['category']}

**Customer tier:** {record['customer_tier']}

**Compensation:** INR {record['compensation']:.2f}

**Outcome:** {record['outcome']}

**Escalated:** {'Yes' if record['escalated'] else 'No'}

**Report:** {record['report']}
"""
        )

    return "\n---\n".join(lines)


# --------------------------------------------------
# PROCESS AN EXCEPTION
# --------------------------------------------------

def submit_exception(report, shipment_value, customer_tier):

    try:

        if not report or not report.strip():
            raise ValueError(
                "Please enter a shipment exception report."
            )

        result = process_exception(
            report=report,
            shipment_value=shipment_value,
            customer_tier=customer_tier
        )

        triage_session.add_record(report, result)

        decision = f"""
## Processing Result

**Category:** {result['category']}

**Customer Tier:** {result['customer_tier']}

**Shipment Value:** INR {result['shipment_value']:.2f}

**Compensation:** INR {result['compensation']:.2f}

**Outcome:** {result['outcome']}

**Escalation Required:** {
    'Yes' if result['escalated'] else 'No'
}

**Escalation Reason:** {
    result['escalation_reason'] or 'Not applicable'
}

### Generated Message

{result['message']}
"""

        steps = "\n".join(
            f"{index}. {step}"
            for index, step in enumerate(
                result["steps"], start=1
            )
        )

        log = format_log(triage_session.get_log())

        return decision, steps, log

    except Exception as exc:

        return (
            f"### Error\n\n{str(exc)}",
            "Processing stopped.",
            format_log(triage_session.get_log())
        )


# --------------------------------------------------
# DAILY SUMMARY
# --------------------------------------------------

def show_summary():

    summary = triage_session.get_summary()

    category_breakdown = summary["category_totals"]

    if category_breakdown:

        category_text = "\n".join(
            f"- **{category}:** INR {amount:.2f}"
            for category, amount
            in category_breakdown.items()
        )

    else:

        category_text = "No category data available."

    return f"""
# Daily Triage Summary

### Overall Statistics

- **Total reports processed:** {summary['total_reports']}
- **Total compensation:** INR {summary['total_compensation']:.2f}
- **Escalated reports:** {summary['escalated_count']}
- **Escalation rate:** {summary['escalation_rate_percent']:.2f}%

### Compensation by Category

{category_text}

### Costliest Category

**Category:** {summary['costliest_category'] or 'N/A'}

**Total Compensation:** INR {summary['costliest_category_total']:.2f}

"""


# --------------------------------------------------
# GRADIO UI
# --------------------------------------------------

with gr.Blocks(
    title="Shipment Exception Desk"
) as demo:

    gr.Markdown(
        """
        # Shipment Exception Desk

        ### Northwind Logistics

        Submit a shipment exception report to classify the
        incident, calculate compensation, and determine
        whether human review is required.
        """
    )

    with gr.Row():

        with gr.Column(scale=1):

            report_input = gr.Textbox(
                label="Shipment Exception Report",
                placeholder=(
                    "Example: The shipment arrived three days late."
                ),
                lines=6
            )

            value_input = gr.Number(
                label="Shipment Value (INR)",
                value=10000,
                minimum=0.01
            )

            tier_input = gr.Radio(
                choices=["standard", "premium"],
                value="standard",
                label="Customer Tier"
            )

            submit_button = gr.Button(
                "Process Exception",
                variant="primary"
            )

        with gr.Column(scale=2):

            result_output = gr.Markdown(
                label="Processing Result"
            )

            steps_output = gr.Markdown(
                label="Processing Steps"
            )

    gr.Markdown("---")

    with gr.Row():

        with gr.Column():

            gr.Markdown("## Daily Triage Log")

            log_output = gr.Markdown(
                value="No exceptions have been processed yet."
            )

        with gr.Column():

            gr.Markdown("## Daily Summary")

            summary_output = gr.Markdown()

            summary_button = gr.Button(
                "Generate Daily Summary"
            )

    submit_button.click(
        fn=submit_exception,
        inputs=[
            report_input,
            value_input,
            tier_input
        ],
        outputs=[
            result_output,
            steps_output,
            log_output
        ]
    )

    summary_button.click(
        fn=show_summary,
        inputs=[],
        outputs=[summary_output]
    )


if __name__ == "__main__":

    demo.launch()