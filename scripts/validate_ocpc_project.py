#!/usr/bin/env python3
"""Compatibility entry point for validating an OCPC project package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ocpc_toolkit import print_result, validate_project


def main() -> int:
    """Validate one public package using the Toolkit v0.2 implementation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="OCPC project package directory")
    args = parser.parse_args()
    return print_result("validate", args.project_dir, validate_project(args.project_dir))


if __name__ == "__main__":
    sys.exit(main())
