#!/usr/bin/env bash
set -euo pipefail
DEMO_REPO=${1:-/tmp/security-patch-agent-demo-repo}
rm -rf "$DEMO_REPO"
mkdir -p "$DEMO_REPO"
cd "$DEMO_REPO"
git init >/dev/null
git config user.name "mayorspride"
git config user.email "mayorspride@gmail.com"
cat > requirements.txt <<'REQ'
flask==2.0.0
requests==2.31.0
REQ
cat > app.py <<'PY'
import hashlib

def fingerprint(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest()
PY
git add . && git commit -m "Create vulnerable demo app" >/dev/null
security-patch-agent --repo "$DEMO_REPO" --apply --report "$DEMO_REPO/security_patch_agent_report.md"
git diff -- .
