import re
from pathlib import Path
from typing import Iterable, List
from packaging.version import Version, InvalidVersion
from .models import Finding

VULNERABLE_DEPS = {
    "flask": {
        "fixed": "2.2.5",
        "severity": "HIGH",
        "title": "Vulnerable Flask dependency version",
        "description": "Flask versions below 2.2.5 are treated as vulnerable by this prototype policy because older pinned versions may include known security fixes missing from the project.",
        "recommendation": "Upgrade Flask to 2.2.5 or newer and run tests before merging.",
    },
    "requests": {
        "fixed": "2.32.4",
        "severity": "MEDIUM",
        "title": "Outdated requests dependency version",
        "description": "Requests versions below 2.32.4 are treated as risky by this prototype policy and should be upgraded to the current safe floor.",
        "recommendation": "Upgrade requests to 2.32.4 or newer and run tests before merging.",
    },
}

RISKY_PATTERNS = [
    {
        "id": "PY-INSECURE-MD5",
        "regex": re.compile(r"hashlib\.md5\("),
        "title": "MD5 hash usage detected",
        "severity": "MEDIUM",
        "description": "MD5 is cryptographically broken and should not be used for security-sensitive hashing.",
        "recommendation": "Replace hashlib.md5 with hashlib.sha256 when compatibility allows.",
    },
    {
        "id": "PY-SUBPROCESS-SHELL-TRUE",
        "regex": re.compile(r"subprocess\.(run|Popen|call|check_call|check_output)\([^\n]*shell\s*=\s*True"),
        "title": "subprocess shell=True usage detected",
        "severity": "HIGH",
        "description": "shell=True may allow command injection when user-controlled input reaches the command string.",
        "recommendation": "Avoid shell=True and pass commands as argument lists; validate or escape user input.",
    },
]

class RepositoryScanner:
    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)

    def scan(self) -> List[Finding]:
        findings: List[Finding] = []
        findings.extend(self._scan_requirements())
        findings.extend(self._scan_python_patterns())
        return findings

    def _scan_requirements(self) -> Iterable[Finding]:
        req = self.repo_path / "requirements.txt"
        if not req.exists():
            return []
        results = []
        for idx, line in enumerate(req.read_text().splitlines(), start=1):
            parsed = re.match(r"^\s*([A-Za-z0-9_.-]+)==([^\s#]+)", line)
            if not parsed:
                continue
            name, version = parsed.group(1).lower(), parsed.group(2)
            if name in VULNERABLE_DEPS:
                try:
                    if Version(version) < Version(VULNERABLE_DEPS[name]["fixed"]):
                        rule = VULNERABLE_DEPS[name]
                        results.append(Finding(
                            id=f"DEP-{name.upper()}-BELOW-{rule['fixed']}",
                            title=rule["title"],
                            severity=rule["severity"],
                            file=req,
                            line=idx,
                            description=f"{rule['description']} Current pin: {name}=={version}.",
                            recommendation=rule["recommendation"],
                        ))
                except InvalidVersion:
                    continue
        return results

    def _scan_python_patterns(self) -> Iterable[Finding]:
        results = []
        for py in self.repo_path.rglob("*.py"):
            if any(part in {".git", ".venv", "venv", "__pycache__"} for part in py.parts):
                continue
            for idx, line in enumerate(py.read_text(errors="ignore").splitlines(), start=1):
                for rule in RISKY_PATTERNS:
                    if rule["regex"].search(line):
                        results.append(Finding(
                            id=rule["id"],
                            title=rule["title"],
                            severity=rule["severity"],
                            file=py,
                            line=idx,
                            description=rule["description"],
                            recommendation=rule["recommendation"],
                        ))
        return results
