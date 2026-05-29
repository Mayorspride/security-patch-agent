from pathlib import Path
from typing import List
from .models import AgentRunResult, Finding, PatchAction

class MarkdownReporter:
    def write(self, result: AgentRunResult, output: Path) -> Path:
        output.parent.mkdir(parents=True, exist_ok=True)
        lines: List[str] = []
        lines.append("# Security Patch Agent Run Report\n")
        lines.append(f"Repository: `{result.repo_path}`")
        lines.append(f"Patch branch: `{result.branch_name}`\n")
        lines.append("## Confirmed Findings\n")
        if not result.findings:
            lines.append("No confirmed findings detected.\n")
        for f in result.findings:
            rel = f.file.relative_to(result.repo_path) if str(f.file).startswith(str(result.repo_path)) else f.file
            lines.append(f"### {f.id}: {f.title}")
            lines.append(f"- Severity: **{f.severity}**")
            lines.append(f"- File: `{rel}` line {f.line}")
            lines.append(f"- Description: {f.description}")
            lines.append(f"- Recommendation: {f.recommendation}\n")
        lines.append("## Patch Plan\n")
        if not result.patch_plan:
            lines.append("No patch plan generated.\n")
        for a in result.patch_plan:
            rel = a.file.relative_to(result.repo_path) if str(a.file).startswith(str(result.repo_path)) else a.file
            lines.append(f"- `{rel}`: {a.summary}")
            lines.append(f"  - Before: `{a.before}`")
            lines.append(f"  - After: `{a.after}`")
        lines.append("\n## Changed Files\n")
        for c in result.changed_files:
            rel = c.relative_to(result.repo_path) if str(c).startswith(str(result.repo_path)) else c
            lines.append(f"- `{rel}`")
        lines.append("\n## Verification\n")
        for v in result.verification:
            lines.append(f"- {v}")
        output.write_text("\n".join(lines) + "\n")
        return output
