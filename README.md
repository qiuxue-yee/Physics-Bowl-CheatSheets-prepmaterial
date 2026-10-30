# Physics Bowl Study Guide & Selected Problems

An independent study project by **Ray Zhou**, bringing concepts, worked
examples and selected PhysicsBowl questions into two connected books.

The guiding idea is simple: a useful formula needs its conditions, a useful
solution needs its reasoning, and a missed question should lead back to the
concept that explains it. The guide keeps the original letter to the reader and
organizes the material around that learning loop.

## Read the books

| Book | Contents | Download |
| --- | --- | --- |
| **Study Guide** | Four parts, 12 units, 48 knowledge points and 71 worked examples | [CheatSheets.pdf](docs/CheatSheets.pdf) |
| **Selected Problems** | 39 topic-indexed questions, key insights, worked solutions and source citations | [Physics_Bowl_Initial_Version.pdf](docs/Physics_Bowl_Initial_Version.pdf) |

The PDFs link to one another. Download them into the same folder; support for
links to another PDF varies by viewer. The [reading page](docs/index.html)
provides a short suggested route through the material.

## What changed in this revision

- Split the large source files into 12 units, four problem groups and shared
  styles, while keeping both PDF filenames and all selected problem numbers.
- Added a topic index and reciprocal links between the guide and problem set.
- Traced all 39 questions to AAPT papers and compared their answer letters to
  the official keys.
- Corrected mismatched figures and several explanations, including the
  short-circuit current comparison, rain relative velocity and incline
  friction. See [REVIEW.md](REVIEW.md) for the full review and remaining work.
- Replaced a PDF-upload-only workflow with builds and checks from LaTeX source.

The earlier revision is preserved in Git history. The project does not claim
unmeasured readership or learning outcomes; feedback and future changes should
be documented with their actual evidence.

| Earlier guide | Revised guide |
| --- | --- |
| ![Earlier kinematics page](docs/previews/guide-before.png) | ![Revised kinematics page](docs/previews/guide-after.png) |

## Project structure

- `guides/physics/CheatSheets.tex` — study guide entry point.
- `guides/physics/units/` — one editable file per unit.
- `Physics_Bowl_Initial_Version.tex` and `problems/` — problem-set entry
  point and question groups.
- `tex/` — shared layout, conventions and generated cross-reference commands.
- `data/problem-topics.json` — the single map between units and problems.
- `data/problem-sources.json` — AAPT paper, question, page and answer-key
  references.
- `docs/` — downloadable PDFs and reading page.
- `tests/` and `scripts/` — integrity, calculation, build and PDF checks.

## Build and verify

Install Python 3 and a TeX Live distribution with pdfLaTeX, common LaTeX
packages, TikZ, tcolorbox and siunitx. Then run from the repository root:

```sh
python -m unittest discover -s tests -v
python scripts/build.py --write-docs
python -m pip install PyMuPDF
python scripts/inspect_pdfs.py
```

The build alternates LaTeX passes so the two books' page references resolve.
It fails on missing references, repeated destinations and LaTeX errors.
`inspect_pdfs.py` additionally verifies every page's text bounds, the
companion-file destinations and all 39 source links. The GitHub Actions
workflow runs these checks and publishes the generated `docs/` folder on
pushes to `main`.

When editing the problem-to-unit mapping or sources, update the JSON files and
run `python scripts/generate_crossrefs.py` before building.

## Sources and attribution

This is an independent, non-official guide. PhysicsBowl is organized by the
American Association of Physics Teachers (AAPT); the project is not endorsed
by AAPT. Selected question statements and some figures originate in AAPT
materials. Each question cites a source paper; see the
[official AAPT exam archive](https://www.aapt.org/Programs/PhysicsBowl/printexams.cfm)
for complete exams and official solutions.

Original explanatory material is shared under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
That license does not grant rights to AAPT's questions or figures.

---

## 中文说明

这是 Ray Zhou 整理的独立 PhysicsBowl 学习资料，包括一本知识手册和一本
精选习题册。项目希望把**公式、适用条件、解题思路和练习**连接起来：
读懂概念，尝试例题，通过习题发现问题，再回到对应知识点复习。

- **知识手册**：四个部分、12 个单元，包含 71 道例题。
- **精选习题**：39 道题，按主题建立索引，提供思路、解答和原题来源。
- **本次整理**：拆分源码，统一符号和排版，加入双向链接，校对题目与
  官方答案，并修复错配图片及部分推导错误。详见 [校对记录](REVIEW.md)。
- **下载**：[知识手册](docs/CheatSheets.pdf) ·
  [精选习题](docs/Physics_Bowl_Initial_Version.pdf)

本项目与 AAPT 无官方隶属关系。AAPT 题目和图片的来源已逐题注明；完整
试卷与官方解答请访问 [AAPT 历年试卷页面](https://www.aapt.org/Programs/PhysicsBowl/printexams.cfm)。
