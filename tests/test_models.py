from secureconfig.models import CheckResult, Severity, Status


def test_result_serialization():
    r=CheckResult("T-1","Example",Severity.LOW,Status.PASS,100,"ok","keep it","Test")
    d=r.to_dict()
    assert d["status"]=="PASS"
    assert d["severity"]=="LOW"
    assert d["score"]==100
