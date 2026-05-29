# Example Pull Request

Title: Apply security patch agent fixes

## Summary

- Upgrades vulnerable Python dependency pins in `requirements.txt`.
- Replaces insecure `hashlib.md5` usage with `hashlib.sha256`.
- Includes generated security patch report and reviewable git diff.

## Validation

- Security Patch Agent completed all five steps.
- Unit tests passed with `pytest -q`.
- `git diff` confirms only small dependency/code changes were made.
