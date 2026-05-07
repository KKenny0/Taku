"""Tests for Windows --strict platform guard in validate_taku.py."""

from __future__ import annotations

import os
import stat
import sys
import tempfile
import textwrap
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_taku import (
    check_compact_source_labels,
    check_evidence_assets,
    check_install_safe_references,
    check_reflect_script,
    check_skill_inventory,
)


def _make_learnings(root: Path, executable: bool = True) -> Path:
    """Create a minimal learnings.py in the expected skill directory."""
    script_dir = root / "skills" / "reflect" / "scripts"
    script_dir.mkdir(parents=True)
    script = script_dir / "learnings.py"
    content = textwrap.dedent("""\
        "add"
        "search"
        "prune"
        "export"
        "bootstrap-check"
        "bootstrap-install"
    """)
    script.write_text(content, encoding="utf-8")
    if executable and os.name != "nt":
        script.chmod(script.stat().st_mode | stat.S_IXUSR)
    return script


def test_strict_windows_skips_executable_bit() -> None:
    """On Windows, --strict should NOT fail on missing executable bit."""
    with tempfile.TemporaryDirectory() as tmp:
        _make_learnings(Path(tmp), executable=False)
        errors: list[str] = []
        with patch("validate_taku.platform.system", return_value="Windows"):
            check_reflect_script(Path(tmp), errors, strict=True)
        assert errors == [], f"Expected no errors on Windows, got: {errors}"


def test_strict_linux_reports_executable_bit() -> None:
    """On Linux, --strict should still report missing executable bit."""
    with tempfile.TemporaryDirectory() as tmp:
        _make_learnings(Path(tmp), executable=False)
        errors: list[str] = []
        with patch("validate_taku.platform.system", return_value="Linux"):
            check_reflect_script(Path(tmp), errors, strict=True)
        assert any("not executable" in e for e in errors), (
            f"Expected 'not executable' error on Linux, got: {errors}"
        )


def test_missing_commands_error_on_all_platforms() -> None:
    """Missing commands should error regardless of platform."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for platform_name in ("Windows", "Linux"):
            script_dir = root / platform_name / "skills" / "reflect" / "scripts"
            script_dir.mkdir(parents=True)
            script = script_dir / "learnings.py"
            script.write_text('# only has "add"\n"add"\n', encoding="utf-8")
            errors: list[str] = []
            with patch("validate_taku.platform.system", return_value=platform_name):
                check_reflect_script(root / platform_name, errors, strict=True)
            missing = [e for e in errors if "missing command" in e]
            assert missing, f"Expected missing-command errors on {platform_name}, got: {errors}"


def test_skill_inventory_requires_exact_taku_commands() -> None:
    """Validator should reject extra installed skill directories."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for skill in ("think", "plan", "build", "review", "debug", "reflect", "compact", "extra"):
            skill_dir = root / "skills" / skill
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("---\nname: taku\n---\n", encoding="utf-8")
        errors: list[str] = []
        check_skill_inventory(root, errors)
        assert any("unexpected skill directory" in e for e in errors), errors


def test_installed_skills_cannot_reference_root_templates() -> None:
    """Installed skills must not depend on root-level runtime templates."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skill_dir = root / "skills" / "think"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "Use templates/design-doc.md as the scaffold.\n",
            encoding="utf-8",
        )
        errors: list[str] = []
        check_install_safe_references(root, errors)
        assert any("non-installed runtime reference" in e for e in errors), errors


def test_compact_source_label_contract_rejects_missing_label() -> None:
    """Compact contracts must expose the strict six-label vocabulary."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in (
            "skills/compact/SKILL.md",
            "skills/compact/references/compact-brief.md",
            "templates/compact-brief.md",
        ):
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Allowed source values: file, git, tool, user, inferred\n", encoding="utf-8")
        errors: list[str] = []
        check_compact_source_labels(root, errors)
        assert any("unknown" in e for e in errors), errors


def test_evidence_assets_require_case_studies() -> None:
    """Evidence assets should include the public case-study evidence wall."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel in (
            "evals/evidence-report.md",
            "scripts/eval_summary.py",
            "scripts/test_eval_summary.py",
            "scripts/test_data/eval_entries.jsonl",
            "CASE_STUDIES.md",
        ):
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
        errors: list[str] = []
        check_evidence_assets(root, errors)
        assert any("expected at least 5 failure-prevention cases" in e for e in errors), errors
