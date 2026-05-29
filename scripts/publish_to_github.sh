#!/usr/bin/env bash
set -euo pipefail
REMOTE_URL=${1:-git@github.com:Mayorspride/security-patch-agent.git}
git init
git branch -M main
git add .
git commit -m "Initial security patch agent prototype"
git remote add origin "$REMOTE_URL"
git push -u origin main
