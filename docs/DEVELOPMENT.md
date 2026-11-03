# Developer notes

| Path | What it contains |
| :--- | :--- |
| `guides/physics/CheatSheets.tex` | Study-guide entry point |
| `guides/physics/units/` | One source file per unit |
| `problems/Physics_Bowl_Initial_Version.tex` | Problem-set entry point |
| `problems/01-10.tex`, etc. | Selected questions and solutions, grouped by number |
| `problems/figures/` | Original question figures; see the folder's notes |
| `Physics_Bowl_Initial_Version.tex` | Compatibility entry point for the previous source path |
| `tex/` and `data/` | Shared styles, conventions, topic map and source records |
| `docs/` | Download page, previews and the two PDFs |
| `scripts/` and `tests/` | Build, integrity, calculation and PDF checks |

Install Python 3 and TeX Live with pdfLaTeX, TikZ, tcolorbox and siunitx. From
the repository root:

```sh
python -m pip install PyMuPDF
python -m unittest discover -s tests -v
python scripts/build.py --write-docs
python scripts/inspect_pdfs.py
python scripts/inspect_pdfs.py --pdf-dir docs --link-mode online --compare-dir .build/online
```

The build alternates LaTeX passes to resolve references between books. The PDF
inspection checks page bounds, companion destinations and source links. The
build verifies the offline PDFs, creates online editions with HTTPS companion
links, checks both forms before publishing, and packages the offline editions
with reading instructions. Tests compare their text, page images and targets.
Integrity tests compare answers against the recorded key data; the editorial
review documents the separate comparison with AAPT's published keys.
When editing the topic map or sources, update the JSON files in `data/` and
run `python scripts/generate_crossrefs.py` before building. GitHub Actions
builds the PDFs on pushes to `main`. The `docs/` reading page is published
when GitHub Pages is enabled for the repository and configured to use GitHub
Actions; otherwise the build still produces the PDF artifacts.

