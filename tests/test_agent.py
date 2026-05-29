from pathlib import Path
from security_patch_agent.scanner import RepositoryScanner
from security_patch_agent.patcher import PatchPlanner, SafePatcher


def test_scanner_finds_vulnerable_dependency_and_md5(tmp_path: Path):
    (tmp_path / "requirements.txt").write_text("flask==2.0.0\n")
    (tmp_path / "app.py").write_text("import hashlib\nhashlib.md5(b'abc').hexdigest()\n")
    findings = RepositoryScanner(tmp_path).scan()
    ids = {f.id for f in findings}
    assert "DEP-FLASK-BELOW-2.2.5" in ids
    assert "PY-INSECURE-MD5" in ids


def test_patcher_updates_files(tmp_path: Path):
    req = tmp_path / "requirements.txt"
    app = tmp_path / "app.py"
    req.write_text("flask==2.0.0\n")
    app.write_text("import hashlib\nhashlib.md5(b'abc').hexdigest()\n")
    findings = RepositoryScanner(tmp_path).scan()
    plan = PatchPlanner().build_plan(findings)
    changed = SafePatcher().apply(plan)
    assert req in changed
    assert app in changed
    assert "flask==2.2.5" in req.read_text()
    assert "hashlib.sha256" in app.read_text()
