#!/usr/bin/env python3
"""Scaffold, validate, and render public OCPC project packages."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import quote

MANIFEST_NAME = "ocpc-project.json"
SUPPORTED_SCHEMA_VERSION = "0.2.0"
REQUIRED_PROJECT_FILES = (
    "README.md",
    "CONTRIBUTORS.md",
    "RISK_AND_PRIVACY.md",
    "PROTOCOL.md",
    "RUBRIC.md",
)
REQUIRED_FIELDS = (
    "schema_version",
    "project_id",
    "title",
    "summary",
    "status",
    "public_issue",
    "maintainers",
    "themes",
    "protocols",
    "licenses",
    "public_artifacts",
    "safety_and_data_release",
    "publication_review",
)
REQUIRED_LICENSE_FIELDS = ("code", "documents", "data")
REQUIRED_SAFETY_FIELDS = (
    "minors_personal_data_included",
    "contact_information_included",
    "precise_locations_included",
    "unauthorized_raw_data_included",
    "public_data_scope",
    "reviewed_by",
    "reviewed_on",
)
REQUIRED_PUBLICATION_REVIEW_FIELDS = (
    "status",
    "reviewed_by",
    "reviewed_on",
    "private_paths_included",
    "minors_original_audio_included",
    "identifiable_conversations_included",
    "withdrawal_mapping_recorded",
)
FORBIDDEN_PUBLIC_DATA_FLAGS = (
    "minors_personal_data_included",
    "contact_information_included",
    "precise_locations_included",
    "unauthorized_raw_data_included",
)
FORBIDDEN_PUBLICATION_FLAGS = (
    "private_paths_included",
    "minors_original_audio_included",
    "identifiable_conversations_included",
)
FORBIDDEN_PUBLIC_PATH_PARTS = {
    "audio-pending",
    "consent",
    "identity",
    "private",
    "raw",
    "registration",
    "withdrawal",
}
ALLOWED_STATUSES = {"draft", "active", "archived"}
ALLOWED_REVIEW_STATUSES = {"draft", "approved"}
PROJECT_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAINTAINER_PATTERN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")


def read_manifest(project_dir: Path) -> tuple[dict[str, Any] | None, list[str]]:
    """Read and parse a project manifest."""
    manifest_path = project_dir / MANIFEST_NAME
    if not manifest_path.is_file():
        return None, [f"missing manifest: {MANIFEST_NAME}"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [
            f"invalid JSON in {MANIFEST_NAME}: line {exc.lineno}, column {exc.colno}"
        ]

    if not isinstance(manifest, dict):
        return None, [f"{MANIFEST_NAME} must contain a JSON object"]
    return manifest, []


def require_non_empty_string(
    container: dict[str, Any], field: str, errors: list[str], prefix: str = ""
) -> None:
    """Require a non-empty string field."""
    value = container.get(field)
    label = f"{prefix}{field}"
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")


def require_string_list(
    container: dict[str, Any], field: str, errors: list[str], prefix: str = ""
) -> None:
    """Require a non-empty list of non-empty strings."""
    value = container.get(field)
    label = f"{prefix}{field}"
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        errors.append(f"{label} must contain at least one non-empty string")


def require_iso_date(
    container: dict[str, Any], field: str, errors: list[str], prefix: str = ""
) -> None:
    """Require an ISO 8601 date string."""
    value = container.get(field)
    label = f"{prefix}{field}"
    if not isinstance(value, str):
        errors.append(f"{label} must be an ISO date")
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{label} must be an ISO date")


def resolve_public_artifact(
    project_dir: Path, artifact_path: str
) -> tuple[Path | None, str | None]:
    """Resolve a declared artifact while keeping it inside the public package."""
    project_root = project_dir.resolve()
    relative_path = Path(artifact_path)
    if relative_path.is_absolute():
        return None, "must be a relative path"

    path_parts = {part.lower() for part in relative_path.parts}
    forbidden_parts = sorted(path_parts & FORBIDDEN_PUBLIC_PATH_PARTS)
    if forbidden_parts:
        return None, f"contains private-only path part: {', '.join(forbidden_parts)}"

    resolved_artifact = (project_root / relative_path).resolve()
    try:
        resolved_artifact.relative_to(project_root)
    except ValueError:
        return None, "must stay inside the project directory"
    return resolved_artifact, None


def validate_manifest(project_dir: Path, manifest: dict[str, Any]) -> list[str]:
    """Validate one parsed OCPC project manifest."""
    errors: list[str] = []
    missing_fields = [field for field in REQUIRED_FIELDS if field not in manifest]
    if missing_fields:
        errors.append(f"missing required fields: {', '.join(missing_fields)}")

    for field in ("schema_version", "project_id", "title", "summary", "public_issue"):
        require_non_empty_string(manifest, field, errors)

    if manifest.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        errors.append(f"schema_version must be {SUPPORTED_SCHEMA_VERSION}")

    project_id = manifest.get("project_id")
    if isinstance(project_id, str) and not PROJECT_ID_PATTERN.fullmatch(project_id):
        errors.append("project_id must use lowercase kebab-case")

    status = manifest.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"status must be one of: {', '.join(sorted(ALLOWED_STATUSES))}")

    maintainers = manifest.get("maintainers")
    if not isinstance(maintainers, list) or not maintainers:
        errors.append("maintainers must contain at least one GitHub account")
    elif any(
        not isinstance(account, str) or not MAINTAINER_PATTERN.fullmatch(account)
        for account in maintainers
    ):
        errors.append("maintainers entries must be valid GitHub account names")

    require_string_list(manifest, "themes", errors)
    require_string_list(manifest, "protocols", errors)

    licenses = manifest.get("licenses")
    if not isinstance(licenses, dict):
        errors.append("licenses must be an object")
    else:
        for field in REQUIRED_LICENSE_FIELDS:
            require_non_empty_string(licenses, field, errors, prefix="licenses.")

    public_artifacts = manifest.get("public_artifacts")
    if not isinstance(public_artifacts, list) or not public_artifacts:
        errors.append("public_artifacts must contain at least one published artifact")
    else:
        for index, artifact in enumerate(public_artifacts):
            label = f"public_artifacts[{index}]"
            if not isinstance(artifact, dict):
                errors.append(f"{label} must be an object")
                continue
            artifact_path = artifact.get("path")
            artifact_type = artifact.get("type")
            if not isinstance(artifact_path, str) or not artifact_path.strip():
                errors.append(f"{label}.path must be a non-empty string")
            else:
                resolved_artifact, resolution_error = resolve_public_artifact(
                    project_dir, artifact_path
                )
                if resolution_error:
                    errors.append(f"{label}.path {resolution_error}: {artifact_path}")
                elif resolved_artifact is not None and not resolved_artifact.is_file():
                    errors.append(f"{label}.path does not exist: {artifact_path}")
            if not isinstance(artifact_type, str) or not artifact_type.strip():
                errors.append(f"{label}.type must be a non-empty string")
            elif artifact_type.lower().startswith("private-"):
                errors.append(f"{label}.type must not publish private artifacts")

    safety = manifest.get("safety_and_data_release")
    if not isinstance(safety, dict):
        errors.append("safety_and_data_release must be an object")
    else:
        for field in REQUIRED_SAFETY_FIELDS:
            if field not in safety:
                errors.append(f"safety_and_data_release.{field} is required")
        for field in FORBIDDEN_PUBLIC_DATA_FLAGS:
            value = safety.get(field)
            if not isinstance(value, bool):
                errors.append(f"safety_and_data_release.{field} must be a boolean")
            elif value:
                errors.append(
                    f"safety_and_data_release.{field} must be false before publication"
                )
        require_non_empty_string(
            safety, "public_data_scope", errors, prefix="safety_and_data_release."
        )
        require_non_empty_string(
            safety, "reviewed_by", errors, prefix="safety_and_data_release."
        )
        require_iso_date(
            safety, "reviewed_on", errors, prefix="safety_and_data_release."
        )

    publication_review = manifest.get("publication_review")
    if not isinstance(publication_review, dict):
        errors.append("publication_review must be an object")
    else:
        for field in REQUIRED_PUBLICATION_REVIEW_FIELDS:
            if field not in publication_review:
                errors.append(f"publication_review.{field} is required")
        review_status = publication_review.get("status")
        if review_status not in ALLOWED_REVIEW_STATUSES:
            errors.append(
                "publication_review.status must be one of: "
                f"{', '.join(sorted(ALLOWED_REVIEW_STATUSES))}"
            )
        require_non_empty_string(
            publication_review, "reviewed_by", errors, prefix="publication_review."
        )
        require_iso_date(
            publication_review, "reviewed_on", errors, prefix="publication_review."
        )
        for field in FORBIDDEN_PUBLICATION_FLAGS:
            value = publication_review.get(field)
            if not isinstance(value, bool):
                errors.append(f"publication_review.{field} must be a boolean")
            elif value:
                errors.append(
                    f"publication_review.{field} must be false before publication"
                )
        withdrawal_mapping = publication_review.get("withdrawal_mapping_recorded")
        if not isinstance(withdrawal_mapping, bool):
            errors.append("publication_review.withdrawal_mapping_recorded must be a boolean")
        elif review_status == "approved" and not withdrawal_mapping:
            errors.append(
                "publication_review.withdrawal_mapping_recorded must be true "
                "before publication"
            )

    for required_file in REQUIRED_PROJECT_FILES:
        if not (project_dir / required_file).is_file():
            errors.append(f"missing required project template: {required_file}")

    return errors


def validate_project(project_dir: Path) -> list[str]:
    """Validate the project directory and return human-readable errors."""
    if not project_dir.is_dir():
        return [f"project directory does not exist: {project_dir}"]
    manifest, errors = read_manifest(project_dir)
    if errors or manifest is None:
        return errors
    return validate_manifest(project_dir, manifest)


def scaffold_project(project_id: str, title: str, output_dir: Path) -> list[str]:
    """Copy the reusable template and personalize its public manifest."""
    errors: list[str] = []
    if not PROJECT_ID_PATTERN.fullmatch(project_id):
        return ["project_id must use lowercase kebab-case"]
    if not title.strip():
        return ["title must be a non-empty string"]
    if output_dir.exists():
        if not output_dir.is_dir():
            return [f"output path must be a directory: {output_dir}"]
        if any(output_dir.iterdir()):
            return [f"output directory must be empty: {output_dir}"]

    template_dir = Path(__file__).resolve().parents[1] / "toolkit" / "templates" / "project"
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template_dir, output_dir, dirs_exist_ok=True)

    manifest_path = output_dir / MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["project_id"] = project_id
    manifest["title"] = title
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return errors


def render_project(project_dir: Path, output_dir: Path) -> list[str]:
    """Render one approved project package as a static public page."""
    manifest, errors = read_manifest(project_dir)
    if errors or manifest is None:
        return errors
    errors.extend(validate_manifest(project_dir, manifest))
    if manifest.get("publication_review", {}).get("status") != "approved":
        errors.append("publication_review.status must be approved before render")
    if errors:
        return errors

    if output_dir.exists():
        if not output_dir.is_dir():
            return [f"output path must be a directory: {output_dir}"]
        if any(output_dir.iterdir()):
            return [f"output directory must be empty: {output_dir}"]
    output_dir.mkdir(parents=True, exist_ok=True)

    artifact_links: list[str] = []
    for artifact in manifest["public_artifacts"]:
        artifact_path = artifact["path"]
        resolved_artifact, resolution_error = resolve_public_artifact(
            project_dir, artifact_path
        )
        if resolution_error or resolved_artifact is None:
            return [f"cannot render artifact {artifact_path}: {resolution_error}"]
        target = output_dir / artifact_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(resolved_artifact, target)
        artifact_links.append(
            "<li><a href=\""
            f"{quote(artifact_path)}\">{html.escape(artifact_path)}</a>"
            f" <span>{html.escape(artifact['type'])}</span></li>"
        )

    themes = "".join(f"<li>{html.escape(theme)}</li>" for theme in manifest["themes"])
    protocols = "".join(
        f"<li>{html.escape(protocol)}</li>" for protocol in manifest["protocols"]
    )
    artifacts = "".join(artifact_links)
    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(manifest["title"])}</title>
  <style>
    body {{ margin: 0; font: 16px/1.65 system-ui, sans-serif; color: #243128; background: #f7f4ec; }}
    main {{ max-width: 900px; margin: 0 auto; padding: 48px 24px 72px; }}
    h1, h2 {{ color: #174f45; }}
    .card {{ margin: 20px 0; padding: 20px; border: 1px solid #c6d4ca; border-radius: 14px; background: #fff; }}
    a {{ color: #176b87; }}
    span {{ color: #66736b; }}
  </style>
</head>
<body>
  <main>
    <p>OCPC / Civic Sensing Lab</p>
    <h1>{html.escape(manifest["title"])}</h1>
    <p>{html.escape(manifest["summary"])}</p>
    <section class="card"><h2>主题 / Themes</h2><ul>{themes}</ul></section>
    <section class="card"><h2>协议 / Protocols</h2><ul>{protocols}</ul></section>
    <section class="card"><h2>公开成果 / Public artifacts</h2><ul>{artifacts}</ul></section>
    <section class="card"><h2>发布边界 / Publication boundary</h2>
      <p>{html.escape(manifest["safety_and_data_release"]["public_data_scope"])}</p>
    </section>
  </main>
</body>
</html>
"""
    (output_dir / "index.html").write_text(page, encoding="utf-8")
    return []


def print_result(action: str, target: Path, errors: list[str]) -> int:
    """Print CLI results consistently."""
    if errors:
        print(f"FAIL: {action} {target}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {action} {target}")
    return 0


def main() -> int:
    """Run the unified CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scaffold_parser = subparsers.add_parser("scaffold", help="Create a project package")
    scaffold_parser.add_argument("project_id")
    scaffold_parser.add_argument("--title", required=True)
    scaffold_parser.add_argument("--output", required=True, type=Path)

    validate_parser = subparsers.add_parser("validate", help="Validate a project package")
    validate_parser.add_argument("project_dir", type=Path)

    render_parser = subparsers.add_parser("render", help="Render an approved static page")
    render_parser.add_argument("project_dir", type=Path)
    render_parser.add_argument("--output", required=True, type=Path)

    args = parser.parse_args()
    if args.command == "scaffold":
        errors = scaffold_project(args.project_id, args.title, args.output)
        return print_result("scaffold", args.output, errors)
    if args.command == "validate":
        errors = validate_project(args.project_dir)
        return print_result("validate", args.project_dir, errors)

    errors = render_project(args.project_dir, args.output)
    return print_result("render", args.output, errors)


if __name__ == "__main__":
    sys.exit(main())
