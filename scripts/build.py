"""Build and cross-link both Physics Bowl PDFs from the repository root."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build" / "pdf"
BOOKS = [
    ("CheatSheets", "guides/physics/CheatSheets.tex"),
    ("Physics_Bowl_Initial_Version", "problems/Physics_Bowl_Initial_Version.tex"),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-docs", action="store_true",
                        help="copy verified PDFs to the existing docs URLs")
    args = parser.parse_args()
    subprocess.run([sys.executable, "scripts/generate_crossrefs.py", "--check"],
                   cwd=ROOT, check=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    if not shutil.which("pdflatex"):
        raise SystemExit("pdflatex was not found. Install TeX Live and retry.")
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "1761258642")
    # The books refer to each other's labels. Alternating passes resolve both
    # page numbers and destinations; the last pass must have no unresolved refs.
    for pass_number in range(1, 4):
        for name, source in BOOKS:
            command = [
                "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                "-file-line-error", f"-output-directory={BUILD}",
                f"-jobname={name}", source,
            ]
            result = subprocess.run(command, cwd=ROOT, env=env,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True,
                                    encoding="utf-8", errors="replace")
            (BUILD / f"{name}.pass{pass_number}.txt").write_text(
                result.stdout, encoding="utf-8")
            if result.returncode:
                print("\n".join(result.stdout.splitlines()[-50:]), file=sys.stderr)
                raise SystemExit(f"{name}: LaTeX failed on pass {pass_number}")
            print(f"{name}: pass {pass_number} complete")
    issues = []
    for name, _ in BOOKS:
        log = (BUILD / f"{name}.log").read_text(encoding="utf-8", errors="replace")
        checks = {
            "undefined references": r"There were undefined references|Reference .+ undefined",
            "duplicate destinations": r"destination with the same identifier",
            "multiply defined labels": r"There were multiply-defined labels",
        }
        issues += [f"{name}: {label}" for label, pattern in checks.items()
                   if re.search(pattern, log)]
    if issues:
        raise SystemExit("PDF verification failed:\n- " + "\n- ".join(issues))
    if args.write_docs:
        for name, _ in BOOKS:
            shutil.copy2(BUILD / f"{name}.pdf", ROOT / "docs" / f"{name}.pdf")
        print("Updated the two existing PDF download paths in docs/.")
    print("Both PDFs compiled with resolved cross-references.")


if __name__ == "__main__":
    main()
