import re
from pathlib import Path
from typing import List
from .models import Finding, PatchAction
from .scanner import VULNERABLE_DEPS

class PatchPlanner:
    def build_plan(self, findings: List[Finding]) -> List[PatchAction]:
        actions: List[PatchAction] = []
        for finding in findings:
            if finding.id.startswith("DEP-"):
                line = finding.file.read_text().splitlines()[finding.line - 1]
                pkg = line.split("==", 1)[0].strip().lower()
                fixed = VULNERABLE_DEPS[pkg]["fixed"]
                actions.append(PatchAction(
                    finding_id=finding.id,
                    file=finding.file,
                    summary=f"Upgrade {pkg} to safe floor {fixed}",
                    before=line,
                    after=f"{pkg}=={fixed}",
                ))
            elif finding.id == "PY-INSECURE-MD5":
                actions.append(PatchAction(
                    finding_id=finding.id,
                    file=finding.file,
                    summary="Replace hashlib.md5 with hashlib.sha256",
                    before="hashlib.md5(",
                    after="hashlib.sha256(",
                ))
        return actions

class SafePatcher:
    def apply(self, actions: List[PatchAction]) -> List[Path]:
        changed = []
        for action in actions:
            content = action.file.read_text()
            if action.finding_id.startswith("DEP-"):
                pattern = re.escape(action.before)
                new_content, count = re.subn(pattern, action.after, content, count=1)
            else:
                new_content, count = content.replace(action.before, action.after), content.count(action.before)
            if count > 0 and new_content != content:
                action.file.write_text(new_content)
                changed.append(action.file)
        return sorted(set(changed))
