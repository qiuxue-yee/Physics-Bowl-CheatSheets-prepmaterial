"""Verify the downloadable bundle corresponds to the published PDF files."""
from pathlib import Path
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'


class ReleaseTests(unittest.TestCase):
    def test_bundle_contains_the_published_books_and_reading_note(self):
        with ZipFile(DOCS / 'PhysicsBowl_Study_Collection.zip') as archive:
            self.assertEqual(set(archive.namelist()), {
                'CheatSheets.pdf', 'Physics_Bowl_Initial_Version.pdf', 'README.txt'
            })
            for name in ('CheatSheets.pdf', 'Physics_Bowl_Initial_Version.pdf'):
                self.assertEqual(archive.read(name), (DOCS / name).read_bytes())
            self.assertIn('same folder', archive.read('README.txt').decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
