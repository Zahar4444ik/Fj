# FSA Assignments - Finite State Automaton Assignment Management System

A comprehensive Python system for generating, managing, and evaluating finite state automaton (FSA) assignments for students. Automates question generation, solution download, evaluation, and result upload to Moodle.

**Status:** ✅ Production Ready | **Python:** 3.13+ 

---

## 🎯 Overview

This system provides an end-to-end solution for managing FSA assignments:

1. **Generate** - Create randomized FSA assignment questions with regex patterns
2. **Download** - Automatically retrieve student submissions from Moodle
3. **Evaluate** - Perform isomorphism checks and behavioral testing on implementations
4. **Upload** - Report grades and feedback back to Moodle
5. **Overview** - Generates testing overview table, that shows every student's task details

**Workflow:**
```
Generate Questions → Download Solutions → Evaluate Implementations → Upload Results
```

---

## ✨ Key Features

### Question Generation
- ✅ Auto-generate FSA questions from regex patterns
- ✅ Randomized difficulty levels
- ✅ Moodle XML export format
- ✅ Configurable number of questions
- ✅ Reference automata generation (DFA/NFA)

### Solution Download
- ✅ Automated Moodle scraping with Selenium
- ✅ Multi-threaded downloads
- ✅ Student metadata extraction
- ✅ Resume capability for interrupted downloads
- ✅ JSON metadata storage

### Solution Evaluation
- ✅ **FSA Specification Checking**
  - Isomorphism verification with reference automaton
  - State annotation validation
  - Alphabet correctness checks
  
- ✅ **Implementation Testing**
  - Static analysis (recursion/iteration detection)
  - Behavioral testing on generated word groups
  - Support for both iterative and recursive implementations
  - DFA and NFA variants
  
- ✅ **Detailed Reporting**
  - Per-student evaluation reports
  - Score breakdown
  - Test case failure analysis

### Result Upload
- ✅ Upload grades to Moodle
- ✅ Attach evaluation reports
- ✅ Batch processing

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- Dependencies from `requirements.txt`

### Installation

```bash
# Clone or download the project
cd fj_assignments

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
cp .env .env

# Edit .env with your settings
# See Configuration section below
```

### Running Commands

```bash
# Generate FSA questions
python main.py generate

# Download student solutions
python main.py download

# Evaluate solutions
python main.py evaluate

# Upload results to Moodle
python main.py upload

# Run full pipeline
python main.py auto

# Generate testing overview
python main.py overview

# Show help
python main.py --help
```

---

## ⚙️ Configuration

Edit `.env` file to configure all settings. All settings are auto-validated - invalid configurations will raise clear error messages.

### Question Generation Settings
```env
# Quiz category in Moodle
QUIZ_CATEGORY="Zapoctovka A/prakticka cast"

# Number of questions to generate
NUMBER_OF_QUESTIONS=10

# Regex difficulty control (number of states)
REGEX_MIN_STATES_COUNT=4
REGEX_MAX_STATES_COUNT=4

# Type of automaton: "dfa", "nfa", or "any"
AUTOMATON_TYPE="any"

# Type of implementation: "iterative", "recursive", or "any"
IMPLEMENTATION_TYPE="any"

# Alphabet size constraints
MAX_ALPHABET_SIZE=3
MIN_ALPHABET_SIZE=3
```

### Question Properties & Evaluation Settings
```env
# Report title/name
REPORT_TITLE="FSA Credit Test A"

# Max points for assignment
ASSIGNMENT_MAX_POINTS=7

# Test configuration
TEST_WORDS_COUNT=30
BAD_WORD_RATIO_LEVEL=0.4
GROUP_SIZE=5
```

### Scoring Configuration - DFA (Deterministic Finite Automaton)
```env
DKA_FSA_ISOMORPHISM=30      # Points for FSA isomorphism check
DKA_FSA_ANNOTATIONS=10      # Points for state annotations
DKA_IMPLEMENTATION=60       # Points for code implementation
# Total: 100 points
```

### Scoring Configuration - NFA (Nondeterministic Finite Automaton)
```env
NKA_FSA_ISOMORPHISM=30      # Points for FSA isomorphism check
NKA_IMPLEMENTATION=70       # Points for code implementation
# Total: 100 points
```

### Moodle Settings
```env
# Moodle credentials
MOODLE_USERNAME="admin"
MOODLE_PASSWORD="your_password"

# Moodle assignment link
ASSIGNMENT_LINK="https://moodle.fei.tuke.sk/mod/quiz/view.php?id=14374"

# Question number to evaluate
QUESTION_NUMBER=1
```

---

## 📊 Project Structure

```
fj_assignments/
├── core/
│   ├── assignment/
│   │   ├── quiz_generator.py        # Generate Moodle XML questions
│   │   ├── assignment_variables.py  # Random assignment generation
│   │   └── utils.py
│   ├── config/
│   │   ├── settings_parse.py        # Load .env configuration
│   │   └── validation.py            # Validate all settings
│   ├── evaluation/
│   │   ├── fsa_evaluation.py        # Evaluate FSA specifications
│   │   ├── implementation_evaluation.py  # Evaluate code implementations
│   │   ├── report.py                # Generate evaluation reports
│   │   └── utils/
│   └── regex/
│       ├── frontend/                # Regex parsing (Lexer/Parser)
│       ├── automata/                # DFA/NFA builders
│       └── generators/              # FSA file generation
├── automated_testing/
│   ├── download_solutions.py        # Download from Moodle
│   ├── solution_evaluation.py       # Evaluate all solutions
│   └── uploading_results.py         # Upload grades to Moodle
├── tasks/
│   ├── task1_isomorphism/           # Isomorphism checking
│   └── task2_behavioral_testing/    # Behavioral testing
├── output/
│   ├── fsa/                         # Generated FSA files
│   ├── automata/                    # Generated automata implementations
│   └── results/                     # Evaluation reports
├── tests/
│   ├── task1/                       # Isomorphism tests
│   └── task2/                       # Implementation tests
├── main.py                          # Entry point
├── .env                             # Configuration (don't commit)
├── requirements.txt                 # Dependencies
└── README.md                        # This file
```

---

## 🔧 Commands Reference

### Generate Questions
```bash
python main.py generate
```
- Generates `NUMBER_OF_QUESTIONS` random FSA questions
- Outputs to `output/quiz.xml`
- Validates configuration before generating
- Creates reference FSA files in `output/fsa/`

### Download Solutions
```bash
python main.py download
```
- Logs into Moodle with provided credentials
- Downloads all student submissions
- Extracts and organizes files by student
- Stores metadata in `students.json`
- Can be resumed if interrupted

### Evaluate Solutions
```bash
python main.py evaluate
```
- Evaluates all downloaded solutions
- Generates per-student evaluation reports
- Performs:
  - FSA isomorphism checks
  - State annotation verification
  - Implementation behavioral testing
- Stores results in `output/results/`

**Evaluation checks:**
- DFA/NFA specification correctness
- Code implementation correctness
- Test case pass/fail analysis

### Upload Results
```bash
python main.py upload
```
- Uploads evaluation results to Moodle
- Attaches detailed reports
- Updates student grades

### Generate Testing Overview
```bash
python main.py overview
```
- Generates CSV table from downloaded student metadata
- Outputs to `output/students_overview.csv`
- Contains columns: email, automaton_type, implementation_type, regex
- Useful for quick review of all student assignments
- Requires `students.json` from download step

### Full Pipeline
```bash
python main.py auto
```
- Runs: Download → Evaluate → Upload
- Complete workflow in one command

### View Help
```bash
python main.py --help
```

---

## 📈 Workflow Example

```bash
# 1. Generate questions
python main.py generate

# 2. Download student solutions
python main.py download

# 3. Evaluate all solutions
python main.py evaluate

# 4. Check results
ls output/results/

# 5. Upload to Moodle
python main.py upload
```

---

## 🔍 Output Files

### Generated Files

| File | Purpose |
|------|---------|
| `output/quiz.xml` | Moodle quiz with generated questions |
| `output/fsa/dka.fsa` | Reference DFA automaton specification |
| `output/fsa/nka.fsa` | Reference NFA automaton specification |
| `output/automata/dka_iterative.py` | DFA iterative implementation |
| `output/automata/dka_recursive.py` | DFA recursive implementation |
| `output/automata/nka_iterative.py` | NFA iterative implementation |
| `output/automata/nka_recursive.py` | NFA recursive implementation |
| `output/results/*.txt` | Evaluation reports per student |
| `output/students_overview.csv` | Student metadata overview table |
| `students.json` | Downloaded metadata |

### Directory Structure

```
output/
├── quiz.xml                    # Generated Moodle quiz
├── fsa/
│   ├── dka.fsa                # DFA specification
│   └── nka.fsa                # NFA specification
├── automata/
│   ├── dka_iterative.py
│   ├── dka_recursive.py
│   ├── nka_iterative.py
│   └── nka_recursive.py
└── results/
    ├── assignment_report.txt
    └── [student_reports]/
```
---

## 🔐 Security Notes

### Environment Variables

Never commit `.env` to version control:
```bash
# Add to .gitignore
echo ".env" >> .gitignore
```

### Moodle Credentials

- Store securely in `.env`
- Don't share `.env` files with others
- Use service accounts if possible
- Rotate passwords periodically
- Don't store credentials in code

### File Access

- Ensure output directories have appropriate permissions
- Don't share evaluation results publicly
- Keep student data private

---

[//]: # (## 📄 License)

[//]: # ()
[//]: # (MIT License - See LICENSE file for details)

[//]: # ()
[//]: # (---)

## 🚀 Getting Started Checklist

- [ ] Python 3.13+ installed
- [ ] Project downloaded/cloned
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created and filled
- [ ] Run `python main.py generate` to test
- [ ] Check `output/quiz.xml` was created
- [ ] Ready to go! 🎉

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-12 | Initial release - Full automation pipeline |

---

## 🎯 Quick Links

- **Main Entry Point:** `main.py`
- **Configuration:** `.env`
- **Question Generator:** `core/assignment/quiz_generator.py`
- **FSA Evaluator:** `core/evaluation/fsa_evaluation.py`
- **Implementation Evaluator:** `core/evaluation/implementation_evaluation.py`

---

## 🤖 Workflow Summary

```
START
  ↓
[Generate] → Create FSA questions, generate reference automata
  ↓
[Download] → Scrape Moodle, extract student solutions
  ↓
[Evaluate] → Check FSA specs, test implementations, grade
  ↓
[Upload] → Send grades and reports back to Moodle
  ↓
COMPLETE
```

---

**Happy automaton grading!** 🤖

For issues or questions, check the troubleshooting section or review code comments.

Last updated: March 12, 2026 | Python 3.13+
