from dataclasses import dataclass, asdict
from enum import Enum


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"
    ERROR = "ERROR"
    NA = "NOT_APPLICABLE"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(frozen=True)
class CheckResult:
    id: str
    title: str
    severity: Severity
    status: Status
    score: int
    evidence: str
    remediation: str
    platform: str

    def to_dict(self):
        data = asdict(self)
        data["severity"] = self.severity.value
        data["status"] = self.status.value
        return data
