"""Run the same economic checks locally and in CI."""

import subprocess
import sys


def main() -> None:
    commands = [
        ["ruff", "check", "apps", "packages", "scripts", "tests"],
        ["ruff", "format", "--check", "apps", "packages", "scripts", "tests"],
        ["mypy"],
        ["pytest"],
    ]
    for command in commands:
        print(f"Running {' '.join(command)}", flush=True)
        result = subprocess.run([sys.executable, "-m", *command], check=False)
        if result.returncode:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
