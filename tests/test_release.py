"""Check the web and offline books have matching content and destinations."""
from pathlib import Path
import sys
import unittest
from zipfile import ZipFile

import fitz

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
sys.path.insert(0, str(ROOT / 'scripts'))
from pdf_links import NAMES, companion_target


def links(doc, expected_mode):
    result = []
    for number, page in enumerate(doc):
        for link in page.get_links():
            target = companion_target(link)
            if target is None:
                continue
            other, destination, mode = target
            if mode != expected_mode:
                raise AssertionError(f'Expected {expected_mode} companion link, got {mode}')
            rect = tuple(round(value, 2) for value in link['from'])
            result.append((number, rect, other, destination))
    return sorted(result)


def other_links(doc):
    result = []
    for number, page in enumerate(doc):
        for link in page.get_links():
            if companion_target(link) is not None:
                continue
            rect = tuple(round(value, 2) for value in link['from'])
            point = link.get('to')
            point = tuple(round(value, 2) for value in point) if point is not None else ()
            result.append((number, rect, link['kind'], link.get('uri', ''),
                           link.get('page', -1), link.get('nameddest', ''), point))
    return sorted(result)


class ReleaseTests(unittest.TestCase):
    def test_bundle_and_web_books_share_content_and_link_destinations(self):
        with ZipFile(DOCS / 'PhysicsBowl_Study_Collection.zip') as archive:
            self.assertEqual(set(archive.namelist()), {*NAMES, 'README.txt'})
            self.assertIn('same folder', archive.read('README.txt').decode('utf-8'))
            for name in NAMES:
                with self.subTest(book=name), \
                     fitz.open(stream=archive.read(name), filetype='pdf') as offline, \
                     fitz.open(DOCS / name) as online:
                    self.assertEqual(len(offline), len(online))
                    for i in range(len(online)):
                        self.assertEqual(offline[i].get_text(), online[i].get_text(), f'{name} page {i+1}')
                    old_links = links(offline, 'offline')
                    new_links = links(online, 'online')
                    self.assertGreaterEqual(len(old_links), 39)
                    self.assertEqual(old_links, new_links)
                    self.assertEqual(other_links(offline), other_links(online))
                    for i in {0, len(online) // 2, len(online) - 1}:
                        self.assertEqual(offline[i].get_pixmap().samples, online[i].get_pixmap().samples,
                                         f'{name} page {i+1} differs visually')


if __name__ == '__main__':
    unittest.main()
