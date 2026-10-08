from secureconfig.checks.windows import firewall, defender_realtime


class FakeRunner:
    def __init__(self, output):
        self.output=output
    def run(self, command, timeout=10):
        return 0,self.output,""


def test_firewall_pass():
    r=FakeRunner('[{"Name":"Domain","Enabled":true},{"Name":"Private","Enabled":true}]')
    assert firewall(r).status.value=="PASS"


def test_firewall_fail():
    r=FakeRunner('[{"Name":"Domain","Enabled":true},{"Name":"Public","Enabled":false}]')
    assert firewall(r).status.value=="FAIL"


def test_defender_pass():
    r=FakeRunner('{"RealTimeProtectionEnabled":true}')
    assert defender_realtime(r).status.value=="PASS"
