import csv
import json
from pathlib import Path


def report_dict(results, score, platform_name):
    counts={}
    for r in results:
        counts[r.status.value]=counts.get(r.status.value,0)+1
    return {
        "platform": platform_name,
        "score": score,
        "summary": counts,
        "checks": [r.to_dict() for r in results],
    }


def write_json(path, payload):
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(path, results):
    fields=["id","title","severity","status","score","evidence","remediation","platform"]
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in results:
            writer.writerow(r.to_dict())
