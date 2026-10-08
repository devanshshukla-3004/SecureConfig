import subprocess
from typing import Sequence


class CommandRunner:
    """Small, testable wrapper around local read-only commands."""

    def run(self, command: Sequence[str], timeout: int = 10) -> tuple[int, str, str]:
        try:
            p = subprocess.run(
                list(command),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            return p.returncode, p.stdout.strip(), p.stderr.strip()
        except (OSError, subprocess.TimeoutExpired) as exc:
            return 1, "", str(exc)
