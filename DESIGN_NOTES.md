# Design Notes

## Key decisions

- **Python CLI prototype:** Python is quick to review, test, and extend for repository automation.
- **Dry-run by default:** The agent must show findings and a patch plan before changing files.
- **Small deterministic patchers:** The prototype upgrades known vulnerable dependency pins and replaces MD5 usage with SHA-256. This keeps patches reviewable and avoids broad code rewrites.
- **Local-first Git model:** The tool prepares a local branch and diff. Users can decide whether to commit, push, and open a pull request.
- **Kubernetes Job deployment:** A batch job fits scheduled scanning and one-off remediation workflows better than a long-running service.

## Limitations

- Vulnerability intelligence is rule-based and intentionally small.
- The scanner does not call external advisory APIs in this prototype.
- It does not automatically run the target repository's tests because executing untrusted code can be risky.
- GitHub PR creation is documented but not performed automatically without a token.
- Pattern fixes may require human review for compatibility-sensitive code.

## Safety controls

- No destructive repository actions.
- No automatic pushes or merges.
- No stored credentials.
- Clear report explaining confirmed findings, assumptions, and actions.
- Rollback steps documented in the README.

## Future improvements

- GitHub App with least-privilege permissions.
- Pull request comments explaining each fix.
- OSV/Semgrep/CodeQL integration.
- Ephemeral sandbox for test execution.
- Configurable policy file for allowed patch types.
- SARIF output for security dashboard integration.
