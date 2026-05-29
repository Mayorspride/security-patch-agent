# Product Requirements Document: Security Patch Agent

## Problem statement

Engineering teams need a safe way to identify common repository security risks, understand the impact, and prepare small reviewable patches without giving an automation tool unlimited authority over source code.

## Target users

- DevOps and platform engineers maintaining many repositories.
- Application teams that need clear remediation guidance.
- Security engineers who want repeatable first-pass remediation workflows.

## Main workflow

1. User points the agent at a GitHub or local repository.
2. Agent inspects repository metadata and files.
3. Agent detects confirmed findings and separates assumptions from evidence.
4. Agent explains vulnerability, severity, and affected file paths.
5. Agent generates a patch plan before changing code.
6. User runs with `--apply` to make safe code or dependency changes.
7. Agent writes a markdown report and leaves a branch/diff ready for review.
8. User may commit, push, and open a pull request.

## In scope

- Local repository inspection.
- Python `requirements.txt` dependency pin scanning.
- Simple risky Python code pattern detection.
- Safe patch planning and small patch application.
- Markdown report generation.
- Kubernetes Job deployment sample.

## Out of scope

- Full SCA database integration.
- Full GitHub App implementation.
- Automatic merge to protected branches.
- Dynamic execution of untrusted repository code.
- Multi-language production-grade patch synthesis.

## Security and privacy requirements

- No secrets or credentials committed to the repository.
- GitHub credentials, when used, must be short-lived or least-privilege tokens.
- Dry-run mode must be default.
- Destructive actions must be avoided.
- The agent must not execute untrusted code unless isolated and explicitly documented.
- Reports should not include secrets found in source code.

## Success criteria

- Detects at least one meaningful issue.
- Explains severity and affected files.
- Produces a patch plan before changes.
- Applies a small safe patch.
- Produces a reviewable diff, branch, or report.
- Provides tests or clear validation steps.
- Can be deployed as a Kubernetes workload.

## Future improvements

- Integrate OSV, Dependabot alerts, CodeQL, Trivy, Semgrep, or GitHub Advanced Security.
- Add GitHub App authentication and automated PR creation.
- Add policy-as-code controls for approved patch types.
- Add container sandboxing for optional test execution.
- Add language-specific patchers for Node, Go, Java, and container images.
