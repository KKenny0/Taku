#!/usr/bin/env python3
"""Validate Taku skill pack consistency without external dependencies."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import stat
import sys
from pathlib import Path

ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
DESCRIPTION_MAX = 1024
PROTOCOL_START = "<!-- TAKU_LEARNINGS_PROTOCOL:START -->"
PROTOCOL_END = "<!-- TAKU_LEARNINGS_PROTOCOL:END -->"
PHASES = ("think", "plan", "build", "review", "debug", "reflect")
EVAL_REQUIRED_FIELDS = {
    "id",
    "title",
    "prompt",
    "expected_phase_route",
    "expected_artifacts",
    "pass_criteria",
    "observed_failure_mode",
}


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    frontmatter = match.group(1)
    body = text[match.end() :]
    values: dict[str, str] = {}
    current_key: str | None = None
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and current_key:
            values[current_key] += "\n" + line.strip()
            continue
        key, _, value = line.partition(":")
        if not key or not _:
            continue
        current_key = key.strip()
        values[current_key] = value.strip().lstrip(">").strip()
    return values, body


def skill_files(root: Path) -> list[Path]:
    return sorted((root / "skills").glob("*/SKILL.md"))


def check_frontmatter(root: Path, errors: list[str]) -> None:
    for path in skill_files(root):
        try:
            frontmatter, _ = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            continue
        unexpected = sorted(set(frontmatter) - ALLOWED_FRONTMATTER_KEYS)
        if unexpected:
            errors.append(f"{path.relative_to(root)}: unexpected frontmatter key(s): {', '.join(unexpected)}")
        name = frontmatter.get("name", "")
        if not re.match(r"^[a-z0-9-]+$", name):
            errors.append(f"{path.relative_to(root)}: invalid skill name: {name!r}")
        description = " ".join(frontmatter.get("description", "").split())
        if not description:
            errors.append(f"{path.relative_to(root)}: missing description")
        if len(description) > DESCRIPTION_MAX:
            errors.append(f"{path.relative_to(root)}: description exceeds {DESCRIPTION_MAX} chars")


def check_review_contract(root: Path, errors: list[str]) -> None:
    path = root / "skills" / "review" / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    forbidden = [
        "Commit auto-fixes " + "atomically",
        "Commit separately",
        "git commit",
        "git add " + "<fixed-files>",
    ]
    for phrase in forbidden:
        if phrase in text:
            errors.append(f"{path.relative_to(root)}: review skill still contains commit instruction: {phrase}")


def check_template_references(root: Path, errors: list[str]) -> None:
    expected = {
        "skills/think/SKILL.md": "templates/design-doc.md",
        "skills/plan/SKILL.md": "templates/plan.md",
        "skills/reflect/SKILL.md": "templates/retro-report.md",
    }
    for skill, template in expected.items():
        text = (root / skill).read_text(encoding="utf-8")
        if template not in text:
            errors.append(f"{skill}: missing template reference to {template}")


def extract_protocol_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(PROTOCOL_START) + r".*?" + re.escape(PROTOCOL_END), re.S)
    return pattern.findall(text)


def check_bootstrap_blocks(root: Path, errors: list[str]) -> None:
    blocks = []
    for name in ("AGENTS.md", "CLAUDE.md"):
        path = root / name
        if not path.exists():
            continue
        found = extract_protocol_blocks(path)
        if len(found) > 1:
            errors.append(f"{name}: contains duplicate Taku learnings protocol blocks")
        blocks.extend(found)
    if blocks and any(block != blocks[0] for block in blocks):
        errors.append("AGENTS.md/CLAUDE.md: Taku learnings protocol blocks differ")


def check_reflect_script(root: Path, errors: list[str], strict: bool) -> None:
    path = root / "skills" / "reflect" / "scripts" / "learnings.py"
    if not path.exists():
        errors.append(f"{path.relative_to(root)}: missing")
        return
    mode = path.stat().st_mode
    if strict and not (mode & stat.S_IXUSR):
        errors.append(f"{path.relative_to(root)}: not executable")
    text = path.read_text(encoding="utf-8")
    for command in ("add", "search", "prune", "export", "bootstrap-check", "bootstrap-install"):
        if f'"{command}"' not in text:
            errors.append(f"{path.relative_to(root)}: missing command {command}")


def check_agents_metadata(root: Path, errors: list[str]) -> None:
    paths = [root / "skills" / phase / "agents" / "openai.yaml" for phase in PHASES]
    for path in paths:
        if not path.exists():
            errors.append(f"{path.relative_to(root)}: missing UI metadata")


def check_trigger_text(root: Path, errors: list[str]) -> None:
    think = (root / "skills" / "think" / "SKILL.md").read_text(encoding="utf-8")
    broad_trigger = "Invoke before ANY " + "build request"
    broad_list = "new feature, component, API, refactor, " + "bug fix"
    if broad_trigger in think or broad_list in think:
        errors.append("skills/think/SKILL.md: trigger description is still too broad")


def check_phase_directories(root: Path, errors: list[str]) -> None:
    for phase in PHASES:
        phase_dir = root / "skills" / phase
        if not phase_dir.is_dir():
            errors.append(f"skills/{phase}: missing phase skill directory")
            continue
        if not (phase_dir / "SKILL.md").is_file():
            errors.append(f"skills/{phase}/SKILL.md: missing phase skill file")
        if not (phase_dir / "agents" / "openai.yaml").is_file():
            errors.append(f"skills/{phase}/agents/openai.yaml: missing phase UI metadata")


def check_evaluation_suite(root: Path, errors: list[str]) -> None:
    path = root / "evals" / "real_task_scenarios.json"
    if not path.exists():
        errors.append(f"{path.relative_to(root)}: missing real-task evaluation suite")
        return
    try:
        scenarios = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(root)}: invalid JSON: {exc}")
        return
    if not isinstance(scenarios, list):
        errors.append(f"{path.relative_to(root)}: top-level value must be a list")
        return
    if len(scenarios) < 6:
        errors.append(f"{path.relative_to(root)}: expected at least 6 scenarios")

    seen_ids: set[str] = set()
    covered_phases: set[str] = set()
    for index, scenario in enumerate(scenarios, start=1):
        label = f"{path.relative_to(root)} scenario {index}"
        if not isinstance(scenario, dict):
            errors.append(f"{label}: scenario must be an object")
            continue
        missing = sorted(EVAL_REQUIRED_FIELDS - set(scenario))
        if missing:
            errors.append(f"{label}: missing field(s): {', '.join(missing)}")
        scenario_id = str(scenario.get("id", ""))
        if not re.match(r"^rt-[0-9]{2}-[a-z0-9-]+$", scenario_id):
            errors.append(f"{label}: invalid id {scenario_id!r}")
        if scenario_id in seen_ids:
            errors.append(f"{label}: duplicate id {scenario_id!r}")
        seen_ids.add(scenario_id)
        for field in EVAL_REQUIRED_FIELDS:
            value = scenario.get(field)
            if isinstance(value, str) and not value.strip():
                errors.append(f"{label}: {field} must not be empty")
            if isinstance(value, list) and not value:
                errors.append(f"{label}: {field} must not be empty")
        for list_field in ("expected_phase_route", "expected_artifacts", "pass_criteria"):
            if list_field in scenario and not isinstance(scenario[list_field], list):
                errors.append(f"{label}: {list_field} must be a list")
        route_value = scenario.get("expected_phase_route", [])
        route = " ".join(route_value) if isinstance(route_value, list) else ""
        for phase in PHASES:
            if f"/taku-{phase}" in route or phase.upper() in route:
                covered_phases.add(phase)
    missing_phase_coverage = sorted(set(PHASES) - covered_phases)
    if missing_phase_coverage:
        errors.append(
            f"{path.relative_to(root)}: scenarios do not cover phase(s): {', '.join(missing_phase_coverage)}"
        )


def check_python_runtime(errors: list[str]) -> None:
    if sys.version_info < (3, 8):
        errors.append(f"Python 3.8+ required; found {platform.python_version()}")


def resolve_expected_target(path: Path) -> Path:
    if path.is_symlink():
        return path.resolve()
    return path


def check_installation(root: Path, skills_dir: Path, errors: list[str], warnings: list[str]) -> None:
    check_python_runtime(errors)
    check_phase_directories(root, errors)
    check_reflect_script(root, errors, strict=True)

    if platform.system() == "Windows":
        warnings.append("Windows installs use junctions; this check verifies targets by path existence.")

    repo_install = skills_dir / "taku"
    if repo_install.exists():
        if resolve_expected_target(repo_install) != root:
            warnings.append(f"{repo_install}: exists but does not resolve to this repo ({root})")
    else:
        warnings.append(f"{repo_install}: not found; skip if you run Taku from another skill directory")

    for phase in PHASES:
        command_path = skills_dir / f"taku-{phase}"
        expected = root / "skills" / phase
        if not command_path.exists():
            errors.append(f"{command_path}: missing slash-command link or junction")
            continue
        resolved = resolve_expected_target(command_path)
        if resolved != expected:
            errors.append(f"{command_path}: resolves to {resolved}, expected {expected}")
        if not (command_path / "SKILL.md").exists():
            errors.append(f"{command_path}: target does not expose SKILL.md")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--install", action="store_true", help="also check local slash-command installation")
    parser.add_argument(
        "--skills-dir",
        default=os.environ.get("TAKU_SKILLS_DIR", str(Path.home() / ".claude" / "skills")),
        help="skills directory to inspect with --install (default: ~/.claude/skills)",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else default_repo_root()
    errors: list[str] = []
    warnings: list[str] = []
    check_phase_directories(root, errors)
    check_frontmatter(root, errors)
    check_review_contract(root, errors)
    check_template_references(root, errors)
    check_bootstrap_blocks(root, errors)
    check_reflect_script(root, errors, args.strict)
    check_agents_metadata(root, errors)
    check_trigger_text(root, errors)
    check_evaluation_suite(root, errors)
    if args.install:
        check_installation(root, Path(args.skills_dir).expanduser().resolve(), errors, warnings)

    if errors:
        print("Taku validation failed:")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")
        return 1
    print("Taku validation passed.")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
