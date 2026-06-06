"""Tests for the zero-dependency OCPC Toolkit v0.2 CLI."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
EXAMPLE_DIR = REPO_ROOT / "examples" / "campus-sensing-combo"
BETA_PROJECT_DIR = REPO_ROOT / "projects" / "campus-sensing-beta-2026-06"
VIBE_PROJECT_DIR = REPO_ROOT / "projects" / "vibe-coding-boundary-sensing"
sys.path.insert(0, str(SCRIPTS_DIR))

import ocpc_toolkit as toolkit  # noqa: E402


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
        self.assertEqual([], toolkit.validate_project(self.project_dir))

    def test_missing_manifest(self) -> None:
        self.manifest_path.unlink()
        self.assertIn(
            "missing manifest: ocpc-project.json",
            toolkit.validate_project(self.project_dir),
        )

    def test_invalid_json(self) -> None:
        self.manifest_path.write_text("{ invalid", encoding="utf-8")
        errors = toolkit.validate_project(self.project_dir)
        self.assertTrue(any("invalid JSON" in error for error in errors))

    def test_missing_required_field(self) -> None:
        manifest = self.read_manifest()
        del manifest["themes"]
        self.write_manifest(manifest)
        errors = toolkit.validate_project(self.project_dir)
        self.assertTrue(any("missing required fields: themes" in error for error in errors))

    def test_unknown_schema_version_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["schema_version"] = "9.9.9"
        self.write_manifest(manifest)
        self.assertIn(
            "schema_version must be 0.2.0",
            toolkit.validate_project(self.project_dir),
        )

    def test_missing_required_template(self) -> None:
        (self.project_dir / "RUBRIC.md").unlink()
        self.assertIn(
            "missing required project template: RUBRIC.md",
            toolkit.validate_project(self.project_dir),
        )

    def test_public_personal_data_is_rejected(self) -> None:
        manifest = copy.deepcopy(self.read_manifest())
        manifest["safety_and_data_release"]["minors_personal_data_included"] = True
        self.write_manifest(manifest)
        self.assertIn(
            "safety_and_data_release.minors_personal_data_included "
            "must be false before publication",
            toolkit.validate_project(self.project_dir),
        )

    def test_artifact_path_outside_project_is_rejected(self) -> None:
        outside_path = self.project_dir.parent / "outside.txt"
        outside_path.write_text("outside project package", encoding="utf-8")
        manifest = self.read_manifest()
        manifest["public_artifacts"].append(
            {"path": "../outside.txt", "type": "invalid-outside-artifact"}
        )
        self.write_manifest(manifest)
        errors = toolkit.validate_project(self.project_dir)
        self.assertTrue(any("must stay inside the project directory" in error for error in errors))

    def test_private_path_is_rejected(self) -> None:
        private_dir = self.project_dir / "private"
        private_dir.mkdir()
        (private_dir / "consent.csv").write_text("private", encoding="utf-8")
        manifest = self.read_manifest()
        manifest["public_artifacts"].append(
            {"path": "private/consent.csv", "type": "documentation"}
        )
        self.write_manifest(manifest)
        errors = toolkit.validate_project(self.project_dir)
        self.assertTrue(any("contains private-only path part" in error for error in errors))

    def test_unreviewed_publication_is_rejected(self) -> None:
        manifest = self.read_manifest()
        manifest["publication_review"]["minors_original_audio_included"] = True
        self.write_manifest(manifest)
        self.assertIn(
            "publication_review.minors_original_audio_included "
            "must be false before publication",
            toolkit.validate_project(self.project_dir),
        )

    def test_approved_publication_requires_withdrawal_mapping(self) -> None:
        manifest = self.read_manifest()
        manifest["publication_review"]["withdrawal_mapping_recorded"] = False
        self.write_manifest(manifest)
        self.assertIn(
            "publication_review.withdrawal_mapping_recorded must be true "
            "before publication",
            toolkit.validate_project(self.project_dir),
        )


class ScaffoldOcpcProjectTests(unittest.TestCase):
    """Cover project package scaffolding."""

    def test_scaffold_personalizes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "new-project"
            self.assertEqual(
                [],
                toolkit.scaffold_project("shade-study", "遮阴观察", output_dir),
            )
            manifest = json.loads(
                (output_dir / "ocpc-project.json").read_text(encoding="utf-8")
            )
            self.assertEqual("shade-study", manifest["project_id"])
            self.assertEqual("遮阴观察", manifest["title"])
            self.assertTrue((output_dir / "PROTOCOL.md").is_file())

    def test_scaffold_rejects_non_empty_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "existing"
            output_dir.mkdir()
            (output_dir / "keep.txt").write_text("keep", encoding="utf-8")
            errors = toolkit.scaffold_project("shade-study", "遮阴观察", output_dir)
            self.assertTrue(any("must be empty" in error for error in errors))


class CampusSensingBetaDraftTests(unittest.TestCase):
    """Keep the real Beta package valid but unpublished until review."""

    def test_beta_draft_package_validates(self) -> None:
        self.assertEqual([], toolkit.validate_project(BETA_PROJECT_DIR))

    def test_beta_draft_package_does_not_render(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "site"
            self.assertIn(
                "publication_review.status must be approved before render",
                toolkit.render_project(BETA_PROJECT_DIR, output_dir),
            )


class VibeCodingBoundaryDraftTests(unittest.TestCase):
    """Keep the Vibe Coding boundary project valid but unpublished until review."""

    def test_vibe_coding_draft_package_validates(self) -> None:
        self.assertEqual([], toolkit.validate_project(VIBE_PROJECT_DIR))

    def test_vibe_coding_draft_package_does_not_render(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "site"
            self.assertIn(
                "publication_review.status must be approved before render",
                toolkit.render_project(VIBE_PROJECT_DIR, output_dir),
            )


class RenderOcpcProjectTests(unittest.TestCase):
    """Cover static HTML rendering."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = Path(self.temp_dir.name) / "project"
        shutil.copytree(EXAMPLE_DIR, self.project_dir)
        self.output_dir = Path(self.temp_dir.name) / "site"
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

    def test_render_copies_public_assets(self) -> None:
        self.assertEqual([], toolkit.render_project(self.project_dir, self.output_dir))
        self.assertTrue((self.output_dir / "index.html").is_file())
        self.assertTrue(
            (self.output_dir / "artifacts" / "synthetic-summary.csv").is_file()
        )

    def test_render_escapes_html(self) -> None:
        manifest = self.read_manifest()
        manifest["title"] = "<script>alert('x')</script>"
        self.write_manifest(manifest)
        self.assertEqual([], toolkit.render_project(self.project_dir, self.output_dir))
        page = (self.output_dir / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_render_rejects_draft_review(self) -> None:
        manifest = self.read_manifest()
        manifest["publication_review"]["status"] = "draft"
        self.write_manifest(manifest)
        self.assertIn(
            "publication_review.status must be approved before render",
            toolkit.render_project(self.project_dir, self.output_dir),
        )

    def test_render_rejects_non_empty_output(self) -> None:
        self.output_dir.mkdir()
        (self.output_dir / "keep.txt").write_text("keep", encoding="utf-8")
        errors = toolkit.render_project(self.project_dir, self.output_dir)
        self.assertTrue(any("must be empty" in error for error in errors))

    def test_compatibility_validator_entry_point(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "validate_ocpc_project.py"),
                str(self.project_dir),
            ],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("OK: validate", result.stdout)


if __name__ == "__main__":
    unittest.main()
