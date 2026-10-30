"""Check every generated page and cross-document PDF destination."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import unquote

try:
    import fitz
except ImportError as exc:
    raise SystemExit("Install PyMuPDF to inspect PDFs: python -m pip install PyMuPDF") from exc

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build/pdf"
NAMES = ("CheatSheets.pdf", "Physics_Bowl_Initial_Version.pdf")


def main() -> None:
    books = {name: fitz.open(BUILD / name) for name in NAMES}
    destinations = {name: set(doc.resolve_names()) for name, doc in books.items()}
    sources = json.loads((ROOT / "data/problem-sources.json").read_text(encoding="utf-8"))
    source_urls = {entry["url"] for entry in sources.values()}
    errors = []
    external = {name: 0 for name in NAMES}
    source_count = 0
    for name, doc in books.items():
        for index, page in enumerate(doc):
            full_text = page.get_text("dict", clip=fitz.INFINITE_RECT())
            for block in full_text["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if not span["text"].strip():
                            continue
                        rect = fitz.Rect(span["bbox"])
                        if (rect.x0 < -0.5 or rect.y0 < -0.5
                                or rect.x1 > page.rect.width + 0.5
                                or rect.y1 > page.rect.height + 0.5):
                            errors.append(f"{name} page {index + 1}: text outside page: {span['text']!r}")
            for link in page.get_links():
                uri = link.get("uri", "")
                if name == NAMES[1] and uri in source_urls:
                    source_count += 1
                target = link.get("file", "")
                if "#nameddest=" not in target:
                    continue
                target_name, destination = target.split("#nameddest=", 1)
                destination = unquote(destination)
                external[name] += 1
                if target_name not in books or destination not in destinations.get(target_name, set()):
                    errors.append(f"{name} page {index + 1}: unresolved {target}")
    if external[NAMES[0]] < 39 or external[NAMES[1]] < 39:
        errors.append(f"Too few reciprocal links: {external}")
    if source_count != 39:
        errors.append(f"Expected 39 source links in problem set; found {source_count}")
    if errors:
        raise SystemExit("\n".join(errors))
    for name, doc in books.items():
        print(f"{name}: {len(doc)} pages, {external[name]} verified companion links")
    print(f"Verified {source_count} AAPT problem-source links and all page bounds.")


if __name__ == "__main__":
    main()
