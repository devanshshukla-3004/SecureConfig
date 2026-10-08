from pathlib import Path
import shutil

from ..models import CheckResult, Severity, Status


def _read(path):
    try:
        return Path(path).read_text(errors="replace")
    except OSError as exc:
        return None, str(exc)


def ssh_root_login():
    path="/etc/ssh/sshd_config"
    text, err=_read(path)
    if text is None:
        return CheckResult("LNX-SSH-001","SSH root login disabled",Severity.HIGH,Status.ERROR,0,err,"Review PermitRootLogin in the SSH server configuration.","Linux")
    values=[]
    for line in text.splitlines():
        s=line.strip()
        if not s or s.startswith("#"): continue
        if s.lower().startswith("permitrootlogin "):
            values.append(s.split(None,1)[1].strip().lower())
    if not values:
        return CheckResult("LNX-SSH-001","SSH root login disabled",Severity.HIGH,Status.WARN,50,"PermitRootLogin is not explicitly configured in sshd_config.","Set PermitRootLogin to no where appropriate and validate the effective SSH configuration.","Linux")
    secure=values[-1] in {"no","prohibit-password","forced-commands-only"}
    return CheckResult("LNX-SSH-001","SSH root login disabled",Severity.HIGH,Status.PASS if secure else Status.FAIL,100 if secure else 0,f"PermitRootLogin={values[-1]}","Disable direct root SSH login unless a documented exception requires it.","Linux")


def firewall():
    tools=[("ufw",["ufw","status"]),("firewalld",["firewall-cmd","--state"]),("nftables",["nft","list","ruleset"])]
    found=[]
    for name,cmd in tools:
        if shutil.which(cmd[0]):
            found.append(name)
    if not found:
        return CheckResult("LNX-FW-001","Host firewall tooling detected",Severity.HIGH,Status.WARN,50,"No supported firewall command was found.","Install and configure a host firewall appropriate to the distribution.","Linux")
    return CheckResult("LNX-FW-001","Host firewall tooling detected",Severity.HIGH,Status.PASS,100,f"Detected firewall tooling: {', '.join(found)}","Verify the detected firewall is enabled and has an appropriate inbound policy.","Linux")


def collect():
    return [firewall(), ssh_root_login()]
