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
from validate_taku import check_reflect_script


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
