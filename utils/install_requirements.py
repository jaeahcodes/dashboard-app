import sys
import subprocess
from pathlib import Path
import argparse

#!/usr/bin/env python3
# installreqs.py — simple installer for requirements.txt


def install(requirements_path: Path) -> int:
    if not requirements_path.exists():
        print(f"requirements file not found: {requirements_path}", file=sys.stderr)
        return 2
    cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)]
    print("Running:", " ".join(cmd))
    try:
        proc = subprocess.run(cmd, check=False)
        return proc.returncode
    except Exception as e:
        print("Installation failed:", e, file=sys.stderr)
        return 1

def main():
    p = argparse.ArgumentParser(description="Install dependencies from requirements.txt")
    p.add_argument("path", nargs="?", default=str(Path(__file__).parent / "requirements.txt"),
                   help="Path to requirements.txt (default: requirements.txt next to this script)")
    args = p.parse_args()
    code = install(Path(args.path))
    sys.exit(code)

if __name__ == "__main__":
    main()