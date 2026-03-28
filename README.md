# FSA Assignments - Finite State Automaton Assignment Management System

A Python system for generating, managing, and evaluating finite state automaton (FSA) assignments for students. Automates question generation, solution download, evaluation, and result upload to Moodle.

**Status:** Production Ready | **Python:** 3.13+

---

## Overview

End-to-end pipeline for managing FSA assignments:

1. **Generate** — Create randomized FSA questions with regex patterns and embed skeleton code
2. **Download** — Automatically retrieve student submissions from Moodle
3. **Evaluate** — Perform isomorphism checks and behavioral testing on implementations
4. **Upload** — Report grades and feedback back to Moodle
5. **Overview** — Generate a CSV table with every student's assignment details

```
Generate Questions → Download Solutions → Evaluate Implementations → Upload Results
```

---

## Key Features

### Question Generation
- Auto-generate FSA questions from regex patterns
- Randomized DFA/NFA with configurable alphabet and state counts
- Moodle XML export with embedded skeleton zip attachments (students get starter code directly in the question)
- Reference automata generation (DFA/NFA)

### Solution Download
- Automated Moodle scraping with Selenium
- Student metadata extraction and JSON storage
- Resume capability for interrupted downloads

### Solution Evaluation
- **FSA Specification Checking** — isomorphism verification, state annotation validation, alphabet correctness
- **Implementation Testing** — static analysis (recursion/iteration detection), behavioral testing on generated word groups, DFA and NFA variants (iterative and recursive)
- **Detailed Reporting** — per-student reports with score breakdown and failure analysis

### Result Upload
- Upload grades and attach evaluation reports to Moodle in batch

---

## Quick Start

### Prerequisites

- Python 3.13+
- Dependencies from `requirements.txt`

### Installation

```bash
cd fj_assignments

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` (or edit `.env` directly) and fill in your settings. See the Configuration section below.

### Commands

```bash
python main.py generate    # Generate Moodle XML quiz questions
python main.py download    # Fetch student submissions from Moodle
python main.py evaluate    # Grade downloaded submissions
python main.py upload      # Send results back to Moodle
python main.py auto        # Full pipeline: download → evaluate → upload
python main.py overview    # Generate students_overview.csv
python main.py --help
```

---

## Configuration

All settings live in `.env`. They are loaded in `core/config/settings_parse.py` and validated in `core/config/validation.py` before any command runs — invalid configurations raise clear error messages.

### Question Generation
```env
QUIZ_CATEGORY="Zapoctovka A/prakticka cast"
NUMBER_OF_QUESTIONS=10

REGEX_MIN_STATES_COUNT=4
REGEX_MAX_STATES_COUNT=4

AUTOMATON_TYPE="any"        # "dfa", "nfa", or "any"
IMPLEMENTATION_TYPE="any"   # "iterative", "recursive", or "any"

MAX_ALPHABET_SIZE=3
MIN_ALPHABET_SIZE=3
```

### Evaluation
```env
REPORT_TITLE="FSA Credit Test A"
ASSIGNMENT_MAX_POINTS=7

TEST_WORDS_COUNT=30
BAD_WORD_RATIO_LEVEL=0.4   # Fraction of non-accepted test words
GROUP_SIZE=5
```

### Scoring

Each group must sum to 100.

```env
# DFA scoring
DKA_FSA_ISOMORPHISM=30
DKA_FSA_ANNOTATIONS=10
DKA_IMPLEMENTATION=60

# NFA scoring
NKA_FSA_ISOMORPHISM=30
NKA_IMPLEMENTATION=70
```

### Moodle
```env
MOODLE_USERNAME="admin"
MOODLE_PASSWORD="your_password"
ASSIGNMENT_LINK="https://moodle.fei.tuke.sk/mod/quiz/view.php?id=14374"
QUESTION_NUMBER=1
HEADLESS=true              # Run browser in headless mode
```

---

## Project Structure

```
fj_assignments/
├── main.py                          # CLI entry point
├── test.py                          # Manual testing script
├── testing_utils.py                 # Helpers for generating automata by regex
│
├── core/
│   ├── assignment/
│   │   ├── quiz_generator.py        # Generate Moodle XML + embed skeleton zips
│   │   └── assignment_variables.py  # Random assignment variable generation
│   ├── config/
│   │   ├── settings_parse.py        # Load .env configuration
│   │   └── validation.py            # Validate all settings
│   ├── evaluation/
│   │   ├── fsa_evaluation.py        # Evaluate FSA specifications (isomorphism, annotations)
│   │   ├── implementation_evaluation.py  # Evaluate code implementations
│   │   └── report.py                # Generate evaluation reports
│   ├── regex/
│   │   ├── frontend/                # ANTLR4-based regex lexer/parser
│   │   ├── automata/                # DFA/NFA builders from parsed regex
│   │   └── generators/              # FSA spec and Python code generators
│   └── summary/
│       └── students_overview_generator.py
│
├── automated_testing/
│   ├── download_solutions.py        # Moodle scraping and zip download
│   ├── evaluate_solutions.py        # Per-student evaluation pipeline
│   └── upload_results.py            # Upload grades to Moodle
│
├── testing/
│   ├── task1_isomorphism/           # Isomorphism checker and FSA generator
│   │   ├── checker/compare.py       # check_isomorphism(), check_annotations()
│   │   └── generator/automata/
│   │       └── canonical.py         # Canonical signature (NFA-safe BFS ordering)
│   └── task2_behavioral_testing/
│       ├── generator/               # Reference implementation generators
│       ├── skeletons/               # Starter code zipped into quiz questions
│       │   ├── skeleton_dfa_iter/
│       │   ├── skeleton_dfa_rec/
│       │   ├── skeleton_nfa_iter/
│       │   └── skeleton_nfa_rec/
│       └── word_generation/         # Accepted/rejected word generators
│
├── tests/
│   ├── task1/
│   │   ├── test_isomorphism.py              # FSA file-based isomorphism tests
│   │   └── test_nfa_isomorphism_stability.py # Multi-run NFA stability tests
│   └── task2/
│       ├── test_dka_iterative.py
│       ├── test_dka_recursive.py
│       ├── test_nka_iterative.py
│       └── test_nka_recursive.py
│
├── output/                          # Generated at runtime, not committed
│   ├── quiz.xml
│   ├── fsa/                         # Reference FSA specs
│   ├── automata/                    # Reference Python implementations
│   └── results/                     # Per-student evaluation reports
│
├── downloads/                       # Student submission zips (not committed)
├── .env                             # Configuration (never commit)
└── requirements.txt
```

---

## Testing

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/task1/test_isomorphism.py
pytest tests/task1/test_nfa_isomorphism_stability.py
pytest tests/task2/test_dka_iterative.py
pytest tests/task2/test_nka_recursive.py
```

`tests/task1/test_nfa_isomorphism_stability.py` specifically covers the NFA canonical signature stability bug — building the same NFA 10 times and verifying all runs are mutually isomorphic.

---

## Output Files

| File | Purpose |
|------|---------|
| `output/quiz.xml` | Moodle quiz with generated questions and skeleton attachments |
| `output/fsa/dka.fsa` | Reference DFA specification |
| `output/fsa/nka.fsa` | Reference NFA specification |
| `output/automata/dka_iterative.py` | Reference DFA iterative implementation |
| `output/automata/dka_recursive.py` | Reference DFA recursive implementation |
| `output/automata/nka_iterative.py` | Reference NFA iterative implementation |
| `output/automata/nka_recursive.py` | Reference NFA recursive implementation |
| `output/results/*.txt` | Evaluation reports per student |
| `output/students_overview.csv` | Student assignment overview |
| `downloads/` | Raw student submission zips |

---

## Security Notes

- Never commit `.env` to version control
- Keep student submission data private
- Use a dedicated Moodle service account if possible

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-12 | Initial release — full automation pipeline |
| 1.1.0 | 2026-03-20 | Skeleton zips embedded in generated quiz questions |
| 1.2.0 | 2026-03-28 | Fix stale .pyc cache causing wrong reference automaton; fix NFA canonical signature non-determinism in isomorphism check; add NFA stability tests |

---

Last updated: March 28, 2026 | Python 3.13+
