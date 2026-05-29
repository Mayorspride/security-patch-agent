import argparse
import os
import subprocess
from pathlib import Path
from .gitops import GitOperations
from .models import AgentRunResult
from .patcher import PatchPlanner, SafePatcher
from .reporter import MarkdownReporter
from .scanner import RepositoryScanner

class SecurityPatchAgent:
    def __init__(self, repo_path: Path, branch_name: str = "security-patch-agent/fixes"):
        self.repo_path = Path(repo_path).resolve()
        self.branch_name = branch_name

    def run(self, apply: bool = False, commit: bool = False, report: Path | None = None) -> AgentRunResult:
        print("[1/5] Inspecting repository")
        git = GitOperations(self.repo_path)
        git.ensure_branch(self.branch_name)

        print("[2/5] Detecting vulnerabilities and risky patterns")
        findings = RepositoryScanner(self.repo_path).scan()
        for finding in findings:
            rel = finding.file.relative_to(self.repo_path)
            print(f"  - CONFIRMED {finding.severity}: {finding.id} in {rel}:{finding.line}")

        print("[3/5] Creating reviewable patch plan")
        plan = PatchPlanner().build_plan(findings)
        for action in plan:
            print(f"  - PLAN {action.summary}: {action.before} -> {action.after}")

        changed = []
        if apply and plan:
            print("[4/5] Applying safe, small patch")
            changed = SafePatcher().apply(plan)
        else:
            print("[4/5] Dry run only; no files changed")

        verification = []
        print("[5/5] Verifying patch result")
        diff = git.diff()
        verification.append("Generated git diff for review" if diff else "No git diff generated")
        if (self.repo_path / "requirements.txt").exists():
            verification.append("requirements.txt present after patch")
        if commit and changed:
            sha = git.commit_if_requested("Apply security patch agent fixes")
            verification.append(f"Created local commit {sha}")
        report_path = report or (self.repo_path / "security_patch_agent_report.md")
        result = AgentRunResult(self.repo_path, self.branch_name, findings, plan, changed, verification)
        MarkdownReporter().write(result, report_path)
        print(f"Report written to {report_path}")
        return result

def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a GitHub/local repository and prepare small security patches.")
    parser.add_argument("--repo", required=True, help="Local repository path. Clone GitHub repos before running or mount them in the container.")
    parser.add_argument("--branch", default="security-patch-agent/fixes", help="Patch branch name")
    parser.add_argument("--apply", action="store_true", help="Apply safe patches. Without this flag the agent performs a dry run.")
    parser.add_argument("--commit", action="store_true", help="Create a local commit after applying patches")
    parser.add_argument("--report", help="Write markdown report to this path")
    args = parser.parse_args()
    SecurityPatchAgent(Path(args.repo), args.branch).run(apply=args.apply, commit=args.commit, report=Path(args.report) if args.report else None)

if __name__ == "__main__":
    main()
