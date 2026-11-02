"""Check every generated page and cross-document PDF destination."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    import fitz
except ImportError as exc:
    raise SystemExit("Install PyMuPDF to inspect PDFs: python -m pip install PyMuPDF") from exc

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build/pdf"
from pdf_links import NAMES, companion_target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf-dir', type=Path, default=BUILD, help='directory containing both PDFs')
    parser.add_argument('--compare-dir', type=Path, help='require byte-identical PDFs in this directory')
    parser.add_argument('--link-mode', choices=('offline', 'online'), default='offline',
                        help='expected type of companion links')
    args = parser.parse_args()
    if args.compare_dir:
        for name in NAMES:
            actual = hashlib.sha256((args.pdf_dir / name).read_bytes()).digest()
            expected = hashlib.sha256((args.compare_dir / name).read_bytes()).digest()
            if actual != expected:
                raise SystemExit(f'{name}: published PDF differs from verified build')
    books = {name: fitz.open(args.pdf_dir / name) for name in NAMES}
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
                target = companion_target(link)
                if target is None:
                    continue
                target_name, destination, mode = target
                external[name] += 1
                if mode != args.link_mode or target_name == name or destination not in destinations.get(target_name, set()):
                    errors.append(f"{name} page {index + 1}: invalid companion link {target}")
    if external[NAMES[0]] < 39 or external[NAMES[1]] < 39:
        errors.append(f"Too few reciprocal links: {external}")
    if source_count != 39:
        errors.append(f"Expected 39 source links in problem set; found {source_count}")
    if errors:
        raise SystemExit("\n".join(errors))
    for name, doc in books.items():
        print(f"{name}: {len(doc)} pages, {external[name]} verified companion links")
    print(f"Verified {source_count} AAPT problem-source links, {args.link_mode} companion links and all page bounds.")


if __name__ == "__main__":
    main()
