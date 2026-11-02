"""Convert companion links for the public web PDFs; retain offline originals."""
from pathlib import Path
from urllib.parse import quote, unquote

import fitz

NAMES = ('CheatSheets.pdf', 'Physics_Bowl_Initial_Version.pdf')
ONLINE_BASE = 'https://qiuxue-yee.github.io/Physics-Bowl-CheatSheets-prepmaterial/'


def companion_target(link):
    """Return (target book, named destination, mode) for a companion link."""
    target = link.get('file', '')
    mode = 'offline'
    if not target:
        target = link.get('uri', '')
        if not target.startswith(ONLINE_BASE):
            return None
        target = target[len(ONLINE_BASE):]
        mode = 'online'
    if '#nameddest=' not in target:
        return None
    name, destination = target.split('#nameddest=', 1)
    return name, unquote(destination), mode


def make_web_books(source_dir: Path, output_dir: Path):
    """Change only remote-GoTo actions to HTTPS links; keep the source intact."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        doc = fitz.open(source_dir / name)
        changed = 0
        try:
            for page in doc:
                for link in page.get_links():
                    target = companion_target(link)
                    if target is None:
                        continue
                    other, destination, mode = target
                    if mode != 'offline' or other not in NAMES or other == name:
                        raise ValueError(f'{name}: unexpected companion link {target}')
                    url = ONLINE_BASE + other + '#nameddest=' + quote(destination, safe='')
                    doc.xref_set_key(link['xref'], 'A', f'<< /S /URI /URI {fitz.get_pdf_str(url)} >>')
                    changed += 1
            if changed < 39:
                raise ValueError(f'{name}: too few companion links to convert ({changed})')
            temporary = output_dir / (name + '.tmp')
            temporary.unlink(missing_ok=True)
            try:
                doc.save(temporary, garbage=3, deflate=True, no_new_id=True)
                temporary.replace(output_dir / name)
            finally:
                temporary.unlink(missing_ok=True)
        finally:
            doc.close()
        print(f'{name}: converted {changed} companion links for online viewing')
