def calculate_delay_compensation(shipment_value: float) -> dict:
    """
    Calculate compensation for a delayed shipment.
    """

    amount = min(shipment_value * 0.05, 1000)

    return {
        "category": "delayed",
        "shipment_value": round(shipment_value, 2),
        "compensation": round(amount, 2),
        "currency": "INR",
        "policy": "5% of shipment value, capped at INR 1000"
    }


def calculate_damage_compensation(shipment_value: float) -> dict:
    """
    Calculate compensation for a damaged shipment.
    """

    amount = min(shipment_value * 0.20, 5000)

    return {
        "category": "damaged",
        "shipment_value": round(shipment_value, 2),
        "compensation": round(amount, 2),
        "currency": "INR",
        "policy": "20% of shipment value, capped at INR 5000"
    }


def calculate_loss_compensation(shipment_value: float) -> dict:
    """
    Calculate compensation for a lost shipment.
    """

    amount = min(shipment_value, 10000)

    return {
        "category": "lost",
        "shipment_value": round(shipment_value, 2),
        "compensation": round(amount, 2),
        "currency": "INR",
        "policy": "100% of shipment value, capped at INR 10000"
    }