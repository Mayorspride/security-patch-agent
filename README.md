<<<<<<< HEAD
# security-patch-agent
A security patch agent that inspect GitHub repositories for security issues, reason about potential fixes, make code changes, and prepare a reviewable patch
=======
# Security Patch Agent

Prototype agent-driven security automation tool that inspects a GitHub or local repository, detects meaningful security issues, explains findings, prepares a patch plan, applies safe changes, and produces a reviewable branch/diff/report.

## What it detects in this prototype

- Vulnerable pinned Python dependencies in `requirements.txt`, including `flask<2.2.5` and `requests<2.32.4`.
- Risky Python code patterns such as `hashlib.md5(` and `subprocess.*(... shell=True ...)`.

## Install

```bash
git clone https://github.com/Mayorspride/security-patch-agent.git
cd security-patch-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

## Run against a local repository

Dry run, no changes:

```bash
security-patch-agent --repo /path/to/repo
```

Apply fixes and write a report:

```bash
security-patch-agent \
  --repo /path/to/repo \
  --branch security-patch-agent/fixes \
  --apply \
  --report /path/to/repo/security_patch_agent_report.md
```

Create a local commit after patching:

```bash
security-patch-agent --repo /path/to/repo --apply --commit
```

Push and open a PR manually:

```bash
cd /path/to/repo
git push origin security-patch-agent/fixes
gh pr create --title "Apply security patch agent fixes" --body-file security_patch_agent_report.md
```

## Test

```bash
pytest -q
```

## Kubernetes deployment

This prototype can run as a Kubernetes `Job`. The sample manifest runs in dry-run mode by default. Mount a repository using a PVC, init container, or ephemeral clone strategy before running in a production environment.

```bash
kubectl create namespace security-patch-agent
kubectl apply -n security-patch-agent -f k8s/configmap.yaml
kubectl apply -n security-patch-agent -f k8s/job.yaml
kubectl logs -n security-patch-agent job/security-patch-agent
```

## Cleanup

Local cleanup:

```bash
deactivate || true
rm -rf .venv .pytest_cache build dist *.egg-info
```

Kubernetes cleanup:

```bash
kubectl delete namespace security-patch-agent
```

Repository rollback:

```bash
cd /path/to/repo
git checkout main
git branch -D security-patch-agent/fixes
```

If a commit was created locally:

```bash
git reset --hard HEAD~1
```

## Safety model

- Dry-run mode is the default.
- The agent prints findings and patch plan before applying changes.
- It keeps patches intentionally small and reviewable.
- It does not commit, push, or open a PR unless explicitly requested or done manually.
- Do not store GitHub tokens in the repository. Use environment variables or Kubernetes secrets with least-privilege scopes.
>>>>>>> 0144945 (Initial commit - Security Patch Agent)
