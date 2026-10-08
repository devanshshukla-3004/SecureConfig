# 🛡️ SecureConfig

> **Day 07 — 100 Days, 100 Cybersecurity Projects**

**SecureConfig** is an offline-first **security configuration auditor** that evaluates a local Windows or Linux host against a small, transparent set of defensive configuration checks.

Instead of changing system settings automatically, it performs **read-only auditing**, produces evidence for every finding, assigns severity and a normalized security score, and provides remediation guidance.

> **Scope:** SecureConfig is a practical security-auditing utility, not a claim of full CIS compliance. CIS Benchmarks are broader secure-configuration guidance maintained across many technology families.

## 🎯 Why this project?

A secure endpoint depends on more than malware detection. Weak host configuration can increase attack surface even when no active compromise is present.

SecureConfig turns common hardening questions into repeatable checks:

```text
Local host
    │
    ▼
Platform detection
    │
    ▼
Read-only configuration checks
    │
    ├──► PASS / FAIL / WARN / ERROR
    │
    ▼
Evidence + remediation
    │
    ▼
Security score
    │
    ├──► Terminal
    ├──► JSON
    └──► CSV
```

## ✨ Current capabilities

| Capability | Description |
|---|---|
| **Windows auditing** | Firewall profiles, Defender real-time protection, UAC |
| **Linux auditing** | SSH root-login policy and firewall tooling detection |
| **Read-only checks** | No configuration changes are performed |
| **Evidence** | Each result records what was observed |
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **Status model** | PASS / FAIL / WARN / ERROR / NOT_APPLICABLE |
| **Security score** | Normalized 0–100 score across evaluated checks |
| **Remediation** | Human-readable guidance accompanies findings |
| **JSON export** | Machine-readable audit report |
| **CSV export** | Spreadsheet/SIEM-friendly result format |
| **Offline-first** | No external security API or network scan required |
| **Testing** | Windows/Linux logic is tested with deterministic fixtures |
| **CI** | Python 3.10–3.13 test matrix |

## 🪟 Windows checks

The Windows implementation uses read-only local inspection:

- Windows Firewall profile state
- Microsoft Defender real-time protection state
- User Account Control (UAC) state

PowerShell is invoked in non-interactive mode and the tool does not execute remediation commands.

## 🐧 Linux checks

The Linux implementation currently checks:

- whether SSH permits direct root login
- whether common host-firewall tooling is present

The Linux checks intentionally avoid modifying `/etc/ssh/sshd_config`, firewall rules, or any other system configuration.

## 📊 Result model

Every check returns a structured record:

```json
{
  "id": "WIN-FW-001",
  "title": "Windows Firewall profiles enabled",
  "severity": "HIGH",
  "status": "PASS",
  "score": 100,
  "evidence": "All reported firewall profiles are enabled.",
  "remediation": "Keep host firewall profiles enabled.",
  "platform": "Windows"
}
```

### Status meanings

| Status | Meaning |
|---|---|
| **PASS** | The checked security condition was satisfied |
| **FAIL** | The condition was not satisfied |
| **WARN** | The tool found an uncertain or lower-confidence condition requiring review |
| **ERROR** | The check could not be evaluated |
| **NOT_APPLICABLE** | The check does not apply to the host |

## 🧮 Security score

The current score is intentionally simple and explainable:

```text
Security Score =
average(score of evaluated checks)
```

A passing check contributes `100`, while a failed check contributes `0`. Warning checks can contribute a partial score.

This is a **triage score**, not a compliance percentage and not a vulnerability score.

## 🚀 Quick start

Requirements:

- Python 3.10+
- Windows PowerShell for Windows checks
- Linux shell environment for Linux checks

```bash
git clone https://github.com/devanshshukla-3004/SecureConfig.git
cd SecureConfig
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
secureconfig
```

Or:

```powershell
python -m secureconfig.cli
```

Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
secureconfig
```

## 📦 Export reports

JSON:

```bash
secureconfig --json reports/secureconfig.json
```

CSV:

```bash
secureconfig --csv reports/secureconfig.csv
```

Both:

```bash
secureconfig --json reports/audit.json --csv reports/audit.csv
```

Automation-friendly:

```bash
secureconfig --json reports/audit.json --quiet
```

The CLI returns a non-zero exit code when an evaluated check fails, making it useful in defensive CI or workstation-baseline workflows.

## 🧪 Testing

```bash
python -m pytest
```

The suite covers:

- result serialization
- report summaries
- Windows firewall parsing
- Defender status parsing
- Linux SSH configuration parsing

CI runs the tests on Python 3.10, 3.11, 3.12, and 3.13.

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │    Local Host        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Platform Detection   │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
       ┌────────────────┐            ┌────────────────┐
       │ Windows Checks │            │  Linux Checks  │
       │ Firewall       │            │ SSH policy     │
       │ Defender       │            │ Firewall tool  │
       │ UAC            │            └───────┬────────┘
       └────────┬───────┘                    │
                └──────────────┬─────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Result + Evidence    │
                    │ Status + Severity    │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Security Score       │
                    └──────────┬───────────┘
                               ▼
                       Terminal / JSON / CSV
```

## 📁 Project structure

```text
SecureConfig/
├── .github/workflows/ci.yml
├── samples/example-report.txt
├── src/secureconfig/
│   ├── checks/
│   │   ├── linux.py
│   │   └── windows.py
│   ├── __init__.py
│   ├── cli.py
│   ├── engine.py
│   ├── models.py
│   ├── reporter.py
│   └── runner.py
├── tests/
│   ├── test_linux.py
│   ├── test_models.py
│   ├── test_reporter.py
│   └── test_windows.py
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## 🔐 Security design

SecureConfig is intentionally conservative:

- no network scanning
- no remote connections
- no automatic remediation
- no downloaded payloads
- no credential collection
- no destructive commands
- no external reputation API
- no configuration writes during an audit

This keeps the tool suitable for defensive learning, local security assessment, and controlled lab environments.

## ⚠️ Limitations

SecureConfig does **not** currently provide:

- complete CIS Benchmark coverage
- enterprise compliance certification
- vulnerability scanning
- malware detection
- network discovery
- automatic hardening
- centralized fleet management
- authentication/RBAC
- cloud configuration auditing

CIS Benchmarks provide broader secure-configuration guidance across many vendor and technology families; SecureConfig intentionally implements only a small, independently testable subset of defensive checks.

## 🗺️ Roadmap

### Current

- [x] Windows configuration auditing
- [x] Linux configuration auditing
- [x] Read-only architecture
- [x] Evidence + remediation
- [x] Severity/status model
- [x] Security score
- [x] JSON/CSV reporting
- [x] Automated tests
- [x] CI matrix

### Planned

- [ ] Expand Windows security checks
- [ ] Expand Linux hardening checks
- [ ] Versioned rule profiles
- [ ] CIS/STIG control mapping
- [ ] HTML audit report
- [ ] Baseline comparison
- [ ] Configuration drift detection
- [ ] Optional remediation mode with explicit confirmation
- [ ] Streamlit security posture dashboard

## 📚 Learning outcomes

Day 07 focuses on:

- host security hardening
- configuration auditing
- platform-specific security controls
- evidence-based findings
- security scoring
- remediation guidance
- safe read-only system inspection
- cross-platform Python architecture
- security automation and CI integration

## 📄 License

MIT License.

## 👨‍💻 Author

**Devansh Shukla**

BTech CSE • Cybersecurity • AI/Data Science

Part of **100 Days, 100 Cybersecurity Projects**.

## ⚖️ Disclaimer

SecureConfig is intended for defensive security research, education, authorized auditing, and controlled environments. Do not modify or assess systems without appropriate authorization.
