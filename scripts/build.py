"""Build and cross-link both Physics Bowl PDFs from the repository root."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build" / "pdf"
BOOKS = [
    ("CheatSheets", "guides/physics/CheatSheets.tex"),
    ("Physics_Bowl_Initial_Version", "problems/Physics_Bowl_Initial_Version.tex"),
]
ZIP_NAME = 'PhysicsBowl_Study_Collection.zip'
README = '''Physics Bowl Study Collection

Keep both PDFs in the same folder so companion links can work.
Support for links to another PDF varies by reader. The guide and problem set
also include topic labels and page references for navigation without links.
In a Chrome online-PDF check, a companion-book link did not open the other
book; use the contents and topic index to navigate manually when needed.

These are independent study materials and are not endorsed by AAPT.
Selected questions and some figures are attributed to AAPT source papers.
'''


def create_archive(directory: Path) -> None:
    """Package exactly the inspected PDFs with a reproducible reading note."""
    temporary = directory / (ZIP_NAME + '.tmp')
    try:
        with ZipFile(temporary, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in [*( (name + '.pdf', (directory / (name + '.pdf')).read_bytes())
                                   for name, _ in BOOKS ), ('README.txt', README.encode('utf-8'))]:
                info = ZipInfo(name, (2025, 10, 23, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=9)
        with ZipFile(temporary) as archive:
            for name, _ in BOOKS:
                if archive.read(name + '.pdf') != (directory / (name + '.pdf')).read_bytes():
                    raise ValueError(f'{name}: archive does not match published PDF')
        temporary.replace(directory / ZIP_NAME)
    finally:
        temporary.unlink(missing_ok=True)


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
    subprocess.run([sys.executable, 'scripts/inspect_pdfs.py', '--pdf-dir', str(BUILD)], cwd=ROOT, check=True)
    if args.write_docs:
        for name, _ in BOOKS:
            shutil.copy2(BUILD / f"{name}.pdf", ROOT / "docs" / f"{name}.pdf")
        subprocess.run([sys.executable, 'scripts/inspect_pdfs.py', '--pdf-dir', str(ROOT / 'docs'),
                        '--compare-dir', str(BUILD)], cwd=ROOT, check=True)
        create_archive(ROOT / 'docs')
        print('Updated the verified PDF download paths and complete collection ZIP in docs/.')
    print("Both PDFs compiled with resolved cross-references.")


if __name__ == "__main__":
    main()
