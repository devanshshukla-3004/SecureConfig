import platform

from .checks import linux, windows
from .models import CheckResult, Status
from .runner import CommandRunner


def collect_checks(runner=None):
    runner = runner or CommandRunner()
    system=platform.system()
    if system == "Windows":
        return windows.collect(runner)
    if system == "Linux":
        return linux.collect()
    return []


def audit(runner=None):
    results=collect_checks(runner)
    evaluated=[r for r in results if r.status not in {Status.NA, Status.ERROR}]
    score=round(sum(r.score for r in evaluated)/len(evaluated)) if evaluated else 0
    return results, score
