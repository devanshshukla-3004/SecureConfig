import json
try:
    import winreg
except ImportError:  # pragma: no cover - non-Windows test environments
    winreg = None

from ..models import CheckResult, Severity, Status


def _ps(runner, script):
    return runner.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script])


def firewall(runner):
    code, out, err = _ps(runner, "(Get-NetFirewallProfile | Select-Object Name,Enabled | ConvertTo-Json -Compress)")
    if code:
        return CheckResult("WIN-FW-001","Windows Firewall profiles enabled",Severity.HIGH,Status.ERROR,0,err or "Unable to query firewall profiles.","Enable Windows Firewall for all active profiles.","Windows")
    try:
        rows = json.loads(out)
        if isinstance(rows, dict): rows=[rows]
        disabled=[x.get("Name","unknown") for x in rows if not x.get("Enabled")]
        if disabled:
            return CheckResult("WIN-FW-001","Windows Firewall profiles enabled",Severity.HIGH,Status.FAIL,0,f"Disabled profiles: {', '.join(disabled)}","Enable Windows Firewall for every profile that should be active.","Windows")
        return CheckResult("WIN-FW-001","Windows Firewall profiles enabled",Severity.HIGH,Status.PASS,100,"All reported firewall profiles are enabled.","Keep host firewall profiles enabled.","Windows")
    except (ValueError, TypeError):
        return CheckResult("WIN-FW-001","Windows Firewall profiles enabled",Severity.HIGH,Status.ERROR,0,"Unexpected PowerShell output.","Review Windows Firewall configuration manually.","Windows")


def defender_realtime(runner):
    code, out, err = _ps(runner, "(Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled | ConvertTo-Json -Compress)")
    if code:
        return CheckResult("WIN-DEF-001","Microsoft Defender real-time protection",Severity.HIGH,Status.ERROR,0,err or "Unable to query Defender status.","Verify Defender real-time protection is enabled.","Windows")
    try:
        enabled=bool(json.loads(out).get("RealTimeProtectionEnabled"))
        return CheckResult("WIN-DEF-001","Microsoft Defender real-time protection",Severity.HIGH,Status.PASS if enabled else Status.FAIL,100 if enabled else 0,f"RealTimeProtectionEnabled={enabled}","Enable Microsoft Defender real-time protection or verify an approved endpoint security control.","Windows")
    except (ValueError, TypeError, AttributeError):
        return CheckResult("WIN-DEF-001","Microsoft Defender real-time protection",Severity.HIGH,Status.ERROR,0,"Unexpected Defender output.","Review endpoint protection status manually.","Windows")


def uac(runner):
    if winreg is None:
        return CheckResult("WIN-UAC-001","User Account Control enabled",Severity.MEDIUM,Status.NA,0,"Windows registry is unavailable on this platform.","Run this check on Windows.","Windows")
    try:
        key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
        value,_=winreg.QueryValueEx(key,"EnableLUA")
        enabled=int(value)==1
        return CheckResult("WIN-UAC-001","User Account Control enabled",Severity.MEDIUM,Status.PASS if enabled else Status.FAIL,100 if enabled else 0,f"EnableLUA={value}","Enable User Account Control (UAC) for elevation prompts.","Windows")
    except OSError as exc:
        return CheckResult("WIN-UAC-001","User Account Control enabled",Severity.MEDIUM,Status.ERROR,0,str(exc),"Review UAC policy in Windows security settings.","Windows")


def collect(runner):
    return [firewall(runner), defender_realtime(runner), uac(runner)]
