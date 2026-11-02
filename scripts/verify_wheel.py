"""Install the built wheel and run tests outside the checkout on Linux or Windows."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    wheels = list((root / "dist").glob("*.whl"))
    if len(wheels) != 1:
        raise SystemExit("Build exactly one wheel in dist/ before verification.")
    with TemporaryDirectory(prefix="stardew-wheel-") as folder:
        work = Path(folder)
        environment = work / "venv"
        subprocess.run(
            ["uv", "venv", "--python", sys.executable, str(environment)], check=True
        )
        python = environment / (
            "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
        )
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                str(python),
                str(wheels[0]) + "[test]",
            ],
            check=True,
        )
        subprocess.run(
            [str(python), "-I", "-m", "stardew", "--version"], cwd=work, check=True
        )
        subprocess.run(
            [str(python), "-I", "-m", "pytest", str(root / "tests"), "-q"],
            cwd=work,
            check=True,
        )


if __name__ == "__main__":
    main()
