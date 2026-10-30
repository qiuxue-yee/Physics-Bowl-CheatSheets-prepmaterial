"""Regression checks against the original structure and AAPT answer keys."""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAP = json.loads((ROOT / "data/problem-topics.json").read_text(encoding="utf-8"))
SOURCES = json.loads((ROOT / "data/problem-sources.json").read_text(encoding="utf-8"))


def problem_blocks() -> dict[int, str]:
    result = {}
    for path in sorted((ROOT / "problems").glob("*.tex")):
        text = path.read_text(encoding="utf-8")
        markers = list(re.finditer(r"(?m)^% Problem (\d+)\s*$", text))
        for index, marker in enumerate(markers):
            number = int(marker.group(1))
            end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
            if number in result:
                raise AssertionError(f"Duplicate problem {number}")
            result[number] = text[marker.start():end]
    return result


class MaterialIntegrityTests(unittest.TestCase):
    def test_units_and_examples_are_preserved(self):
        units = sorted((ROOT / "guides/physics/units").glob("*.tex"))
        self.assertEqual(len(units), 12)
        example_counts = []
        labels = set()
        point_count = 0
        for unit in units:
            text = unit.read_text(encoding="utf-8")
            label = re.search(r"\\label\{unit:([^}]+)\}", text)
            self.assertIsNotNone(label, unit)
            self.assertNotIn(label.group(1), labels)
            labels.add(label.group(1))
            point_count += text.count(r"\begin{KnowledgePoint}")
            starts = text.count(r"\begin{cheatproblem}")
            self.assertEqual(starts, text.count(r"\end{cheatproblem}"), unit)
            for example in re.findall(
                r"\\begin\{cheatproblem\}(.*?)\\end\{cheatproblem\}", text, re.S
            ):
                self.assertIn(r"\begin{solutionbox}", example, unit)
            example_counts.append(starts)
        self.assertEqual(labels, {u["id"] for u in MAP["units"]})
        self.assertEqual(point_count, 48)
        self.assertEqual(example_counts, [10, 8, 6, 8, 8, 5, 7, 4, 4, 5, 4, 2])

    def test_all_questions_have_sources_and_match_official_answer_keys(self):
        problems = problem_blocks()
        self.assertEqual(set(problems), set(range(1, 40)))
        self.assertEqual(set(SOURCES), {str(i) for i in problems})
        for number, block in problems.items():
            with self.subTest(problem=number):
                source = SOURCES[str(number)]
                self.assertEqual(block.count(r"\label{prob:" + str(number) + "}"), 1)
                self.assertIn(r"\StudyGuideLinks{" + str(number) + "}", block)
                self.assertIn(r"\ProblemSource{" + str(number) + "}", block)
                self.assertIn(r"\begin{insightbox}", block)
                self.assertIn(r"\begin{solutionbox}", block)
                answer = re.search(r"\\finalanswer\{\(([A-E])\)", block)
                self.assertIsNotNone(answer)
                self.assertEqual(answer.group(1), source["official_answer"])
                self.assertTrue(source["url"].startswith("https://www.aapt.org/"))
                self.assertTrue(source["solutions_url"].startswith("https://www.aapt.org/"))
                self.assertGreater(source["pdf_page"], 0)

    def test_figures_are_present_and_corrected_mismatches_stay_fixed(self):
        problems = problem_blocks()
        for number, block in problems.items():
            for filename in re.findall(r"\\includegraphics(?:\[[^]]+\])?\{([^}]+)\}", block):
                with self.subTest(problem=number, filename=filename):
                    self.assertTrue((ROOT / filename).is_file())
        expected = {
            22: "Problem_21_Figure.png",
            23: "Problem_23_Figure.png",
            28: "Problem_28_Figure.png",
            29: "Problem_29_Figure.png",
            36: "Problem_31_Figure.png",
        }
        for number, filename in expected.items():
            self.assertIn(filename, problems[number])
        self.assertIn(r"\begin{tikzpicture}", problems[27])
        self.assertNotIn("Problem_28_Figure.png", problems[27])


if __name__ == "__main__":
    unittest.main()
