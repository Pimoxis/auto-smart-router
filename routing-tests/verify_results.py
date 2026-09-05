"""Verify live extraction independently, using integer arithmetic."""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

root = Path(__file__).resolve().parent
totals = defaultdict(lambda: {"count": 0, "amount_cents": 0})
void_ids = []
with (root / "invoices.csv").open(newline="", encoding="utf-8") as source:
    for row in csv.DictReader(source):
        if row["status"] == "void":
            void_ids.append(row["id"])
        else:
            totals[row["department"]]["count"] += 1
            totals[row["department"]]["amount_cents"] += int(row["amount_cents"])
expected = {"departments": dict(totals), "void_ids": void_ids,
            "grand_total_cents": sum(x["amount_cents"] for x in totals.values()),
            "paid_count": sum(x["count"] for x in totals.values())}
if __name__ == "__main__":
    result_path = root / (sys.argv[1] if len(sys.argv) > 1 else "extraction.json")
    if result_path.exists():
        actual = json.loads(result_path.read_text(encoding="utf-8-sig"))
        assert actual == expected, {"actual": actual, "expected": expected}
        print("PASS: every department count, sum, void ID, and grand total matches.")
    else:
        print(json.dumps(expected, indent=2))
