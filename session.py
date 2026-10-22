from collections import defaultdict
from threading import RLock


class TriageSession:

    def __init__(self):
        self.records = []
        self.lock = RLock()

    def add_record(self, report: str, result: dict) -> dict:

        with self.lock:

            record = {
                "report": report,
                **result
            }

            self.records.append(record)

            return record

    def get_log(self) -> list:

        with self.lock:
            return list(self.records)

    def get_summary(self) -> dict:

        with self.lock:

            records = list(self.records)

        total_reports = len(records)

        total_compensation = sum(
            record["compensation"]
            for record in records
        )

        escalated_count = sum(
            1
            for record in records
            if record["escalated"]
        )

        escalation_rate = (
            escalated_count / total_reports * 100
            if total_reports
            else 0.0
        )

        category_totals = defaultdict(float)

        for record in records:

            category = record["category"]

            category_totals[category] += (
                record["compensation"]
            )

        if category_totals:

            costliest_category = max(
                category_totals,
                key=category_totals.get
            )

            costliest_category_total = (
                category_totals[costliest_category]
            )

        else:

            costliest_category = None
            costliest_category_total = 0.0

        return {
            "total_reports": total_reports,
            "total_compensation": round(
                total_compensation, 2
            ),
            "escalated_count": escalated_count,
            "escalation_rate_percent": round(
                escalation_rate, 2
            ),
            "category_totals": {
                category: round(amount, 2)
                for category, amount
                in category_totals.items()
            },
            "costliest_category": costliest_category,
            "costliest_category_total": round(
                costliest_category_total, 2
            )
        }


# Shared session for the Gradio application.

triage_session = TriageSession()