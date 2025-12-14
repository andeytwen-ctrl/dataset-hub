"""
Sphinx documentation build helper.

This script builds the documentation by temporarily installing the project
into the active virtual environment, running ``sphinx-build``, and then
uninstalling the project.

This approach is intentional: when using Sphinx with MyST-NB, notebooks
included from outside the ``docs/`` directory (via ``.. include::``) may not
fully respect ``conf.py`` configuration and may fail to resolve project
imports unless the project is installed.

This is a known limitation of MyST-NB:
https://github.com/executablebooks/MyST-NB/issues/583

Installing the project ensures a stable and user-equivalent execution
environment for notebook execution during the documentation build.

Usage
-----
Run this script from the project root or via:

    python docs/build.py
"""

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    print(f"\n$ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    docs_dir = project_root / "docs"
    build_dir = project_root / "_build"

    try:
        run([sys.executable, "-m", "pip", "install", "-e", "."], cwd=project_root)

        run(
            [
                "sphinx-build",
                "-b",
                "html",
                str(docs_dir),
                str(build_dir),
            ],
            cwd=project_root,
        )

    finally:
        run(
            [sys.executable, "-m", "pip", "uninstall", "-y", "my-project-name"],
            cwd=project_root,
        )


if __name__ == "__main__":
    main()
