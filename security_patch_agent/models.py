from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

@dataclass
class Finding:
    id: str
    title: str
    severity: str
    file: Path
    line: Optional[int]
    description: str
    recommendation: str
    confirmed: bool = True

@dataclass
class PatchAction:
    finding_id: str
    file: Path
    summary: str
    before: str
    after: str

@dataclass
class AgentRunResult:
    repo_path: Path
    branch_name: str
    findings: List[Finding] = field(default_factory=list)
    patch_plan: List[PatchAction] = field(default_factory=list)
    changed_files: List[Path] = field(default_factory=list)
    verification: List[str] = field(default_factory=list)
