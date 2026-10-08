import argparse
import platform

from .engine import audit
from .models import Status
from .reporter import report_dict, write_csv, write_json


def main():
    p=argparse.ArgumentParser(description="SecureConfig - offline security configuration auditor")
    p.add_argument("--json", metavar="PATH", help="write a JSON report")
    p.add_argument("--csv", metavar="PATH", help="write a CSV report")
    p.add_argument("--quiet", action="store_true", help="suppress the terminal table")
    args=p.parse_args()

    results, score=audit()
    payload=report_dict(results,score,platform.system())

    if not args.quiet:
        print(f"SECURECONFIG | {platform.system()} | SCORE {score}/100")
        print("-"*92)
        print(f"{'ID':<15} {'STATUS':<16} {'SEV':<9} {'SCORE':<7} TITLE")
        print("-"*92)
        for r in results:
            print(f"{r.id:<15} {r.status.value:<16} {r.severity.value:<9} {r.score:<7} {r.title}")
            print(f"  Evidence: {r.evidence}")
            print(f"  Fix:      {r.remediation}")
        print("-"*92)
        print(f"{len(results)} check(s) | PASS={payload['summary'].get('PASS',0)} FAIL={payload['summary'].get('FAIL',0)} WARN={payload['summary'].get('WARN',0)} ERROR={payload['summary'].get('ERROR',0)}")

    if args.json: write_json(args.json,payload)
    if args.csv: write_csv(args.csv,results)

    return 0 if not any(r.status == Status.FAIL for r in results) else 2
