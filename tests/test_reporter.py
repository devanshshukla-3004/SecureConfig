from secureconfig.models import CheckResult, Severity, Status
from secureconfig.reporter import report_dict


def test_report_summary():
    rs=[
        CheckResult("1","A",Severity.HIGH,Status.PASS,100,"e","r","Test"),
        CheckResult("2","B",Severity.MEDIUM,Status.FAIL,0,"e","r","Test"),
    ]
    p=report_dict(rs,50,"Test")
    assert p["score"]==50
    assert p["summary"]=={"PASS":1,"FAIL":1}
    assert len(p["checks"])==2
