from pipeline import process_exception


TEST_CASES = [
    {
        "name": "Mild delay",
        "report": (
            "The shipment arrived one day later than expected."
        ),
        "shipment_value": 1000,
        "customer_tier": "standard",
        "expected_category": "delayed",
        "expected_escalation": False
    },
    {
        "name": "High-value loss",
        "report": (
            "The shipment has been lost in transit "
            "and cannot be located."
        ),
        "shipment_value": 50000,
        "customer_tier": "standard",
        "expected_category": "lost",
        "expected_escalation": True
    },
    {
        "name": "Minor damage",
        "report": (
            "One item in the shipment arrived with "
            "minor packaging damage."
        ),
        "shipment_value": 1000,
        "customer_tier": "standard",
        "expected_category": "damaged",
        "expected_escalation": False
    },
    {
        "name": "Garbled report",
        "report": (
            "blue seven tomorrow broken maybe parcel "
            "window 42 sideways"
        ),
        "shipment_value": 100,
        "customer_tier": "standard",
        "expected_category": "unknown",
        "expected_escalation": True
    }
]


def run_checks():

    passed = 0

    for case in TEST_CASES:

        print(f"\nTesting: {case['name']}")

        result = process_exception(
            report=case["report"],
            shipment_value=case["shipment_value"],
            customer_tier=case["customer_tier"]
        )

        category_ok = (
            result["category"]
            == case["expected_category"]
        )

        escalation_ok = (
            result["escalated"]
            == case["expected_escalation"]
        )

        success = category_ok and escalation_ok

        print("Expected category:", case["expected_category"])
        print("Actual category:", result["category"])

        print(
            "Expected escalation:",
            case["expected_escalation"]
        )

        print(
            "Actual escalation:",
            result["escalated"]
        )

        print("Result:", "PASS" if success else "FAIL")

        if success:
            passed += 1

    print(f"\nFinal score: {passed}/{len(TEST_CASES)}")

    if passed != len(TEST_CASES):
        raise SystemExit("One or more triage checks failed.")


if __name__ == "__main__":
    run_checks()