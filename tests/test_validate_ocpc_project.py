"""Tests for the zero-dependency OCPC project validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ocpc_project.py"
EXAMPLE_DIR = REPO_ROOT / "examples" / "campus-sound-map"

SPEC = importlib.util.spec_from_file_location("validate_ocpc_project", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateOcpcProjectTests(unittest.TestCase):
    """Cover successful validation and publication-blocking errors."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = Path(self.temp_dir.name) / "project"
        shutil.copytree(EXAMPLE_DIR, self.project_dir)
        self.manifest_path = self.project_dir / "ocpc-project.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def read_manifest(self) -> dict[str, Any]:
        """Read the temporary manifest."""
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, manifest: dict[str, Any]) -> None:
        """Write the temporary manifest."""
        self.manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_valid_example(self) -> None:
        self.assertEqual([], VALIDATOR.validate_project(self.project_dir))

    def test_missing_manifest(self) -> None:
        self.manifest_path.unlink()
        self.assertIn(
            "missing manifest: ocpc-project.json",
            VALIDATOR.validate_project(self.project_dir),
        )

    def test_invalid_json(self) -> None:
        self.manifest_path.write_text("{ invalid", encoding="utf-8")
        errors = VALIDATOR.validate_project(self.project_dir)
        self.assertTrue(any("invalid JSON" in error for error in errors))

    def test_missing_required_field(self) -> None:
        manifest = self.read_manifest()
        del manifest["public_issue"]
        self.write_manifest(manifest)
        errors = VALIDATOR.validate_project(self.project_dir)
        self.assertTrue(any("missing required fields: public_issue" in error for error in errors))

    def test_unknown_schema_version_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["schema_version"] = "9.9.9"
        self.write_manifest(manifest)
        errors = VALIDATOR.validate_project(self.project_dir)
        self.assertIn("schema_version must be 0.1.0", errors)

    def test_missing_required_template(self) -> None:
        (self.project_dir / "RISK_AND_PRIVACY.md").unlink()
        errors = VALIDATOR.validate_project(self.project_dir)
        self.assertIn(
            "missing required project template: RISK_AND_PRIVACY.md",
            errors,
        )

    def test_missing_safety_statement(self) -> None:
        manifest = self.read_manifest()
        del manifest["safety_and_data_release"]
        self.write_manifest(manifest)
        errors = VALIDATOR.validate_project(self.project_dir)
        self.assertTrue(
            any("missing required fields: safety_and_data_release" in error for error in errors)
        )

    def test_public_personal_data_is_rejected(self) -> None:
        manifest = copy.deepcopy(self.read_manifest())
        manifest["safety_and_data_release"]["minors_personal_data_included"] = True
        self.write_manifest(manifest)
        errors = VALIDATOR.validate_project(self.project_dir)
        self.assertIn(
            "safety_and_data_release.minors_personal_data_included "
            "must be false before publication",
            errors,
        )

    def test_artifact_path_outside_project_is_rejected(self) -> None:
        outside_path = self.project_dir.parent / "outside.txt"
        outside_path.write_text("outside project package", encoding="utf-8")
        manifest = self.read_manifest()
        manifest["public_artifacts"].append(
            {
                "path": "../outside.txt",
                "type": "invalid-outside-artifact",
            }
        )
        self.write_manifest(manifest)
        errors = VALIDATOR.validate_project(self.project_dir)
        self.assertIn(
            "public_artifacts[4].path must stay inside the project directory: "
            "../outside.txt",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
