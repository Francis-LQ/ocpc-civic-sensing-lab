#!/usr/bin/env python3
"""Validate an OCPC project package without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MANIFEST_NAME = "ocpc-project.json"
SUPPORTED_SCHEMA_VERSION = "0.1.0"
REQUIRED_PROJECT_FILES = (
    "README.md",
    "CONTRIBUTORS.md",
    "RISK_AND_PRIVACY.md",
)
REQUIRED_FIELDS = (
    "schema_version",
    "project_id",
    "title",
    "summary",
    "status",
    "public_issue",
    "maintainers",
    "licenses",
    "public_artifacts",
    "safety_and_data_release",
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
FORBIDDEN_PUBLIC_DATA_FLAGS = (
    "minors_personal_data_included",
    "contact_information_included",
    "precise_locations_included",
    "unauthorized_raw_data_included",
)
ALLOWED_STATUSES = {"draft", "active", "archived"}
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
        project_root = project_dir.resolve()
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
                resolved_artifact = (project_dir / artifact_path).resolve()
                try:
                    resolved_artifact.relative_to(project_root)
                except ValueError:
                    errors.append(
                        f"{label}.path must stay inside the project directory: "
                        f"{artifact_path}"
                    )
                else:
                    if not resolved_artifact.is_file():
                        errors.append(f"{label}.path does not exist: {artifact_path}")
            if not isinstance(artifact_type, str) or not artifact_type.strip():
                errors.append(f"{label}.type must be a non-empty string")

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
        for field in ("public_data_scope", "reviewed_by", "reviewed_on"):
            require_non_empty_string(
                safety, field, errors, prefix="safety_and_data_release."
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


def main() -> int:
    """Run the CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="OCPC project package directory")
    args = parser.parse_args()

    errors = validate_project(args.project_dir)
    if errors:
        print(f"FAIL: {args.project_dir}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: {args.project_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
