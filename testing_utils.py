"""
Testing Utilities for FSA and Automata Generation

Simple functions for generating FSA and automata files from regex patterns.
"""

from pathlib import Path

from core.config.settings_parse import REGEX_MIN_STATES_COUNT, REGEX_MAX_STATES_COUNT
from core.regex.frontend.helper import get_ast_from_regex
from core.regex.automata.dka.dka_builder import build_DKA
from core.regex.automata.nka.nka_builder import build_NKA
from core.regex.generators.fsa.fsa_generator import fsa_from_dka, fsa_from_nka
from core.regex.generators.regex.random_regex import generate_assignment_regexes
from testing.task2_behavioral_testing.generator.dka.iterative import generate_iterative_dka
from testing.task2_behavioral_testing.generator.dka.recursive import generate_recursive_dka
from testing.task2_behavioral_testing.generator.nka.iterative import generate_iterative_nka
from testing.task2_behavioral_testing.generator.nka.recursive import generate_recursive_nka

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
FSA_DIR = OUTPUT_DIR / "fsa"
AUTOMATA_DIR = OUTPUT_DIR / "automata"

FSA_DIR.mkdir(parents=True, exist_ok=True)
AUTOMATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_fsa(regex: str) -> dict:
    """
    Generate FSA files (dka.fsa and nka.fsa) from regex.

    Files saved to: output/fsa/dka.fsa and output/fsa/nka.fsa

    Args:
        regex: Regex pattern string

    Returns:
        dict: {"dfa": Path, "nfa": Path}
    """
    ast = get_ast_from_regex(regex)

    dka = build_DKA(ast, regex)
    fsa_from_dka(dka, filename=str(FSA_DIR / "dka.fsa"))

    nka = build_NKA(ast)
    fsa_from_nka(nka, filename=str(FSA_DIR / "nka.fsa"))

    return {
        "dfa": FSA_DIR / "dka.fsa",
        "nfa": FSA_DIR / "nka.fsa"
    }


def generate_automata(regex: str) -> dict:
    """
    Generate all automata implementations from regex.

    Files saved to output/automata/:
    - dka_iterative.py
    - dka_recursive.py
    - nka_iterative.py
    - nka_recursive.py

    Args:
        regex: Regex pattern string

    Returns:
        dict: {"dfa_iterative": Path, "dfa_recursive": Path, "nfa_iterative": Path, "nfa_recursive": Path}
    """
    ast = get_ast_from_regex(regex)

    generate_iterative_dka(ast, path=str(AUTOMATA_DIR / "dka_iterative.py"))
    generate_recursive_dka(ast, path=str(AUTOMATA_DIR / "dka_recursive.py"))
    generate_iterative_nka(ast, path=str(AUTOMATA_DIR / "nka_iterative.py"))
    generate_recursive_nka(ast, path=str(AUTOMATA_DIR / "nka_recursive.py"))

    return {
        "dfa_iterative": AUTOMATA_DIR / "dka_iterative.py",
        "dfa_recursive": AUTOMATA_DIR / "dka_recursive.py",
        "nfa_iterative": AUTOMATA_DIR / "nka_iterative.py",
        "nfa_recursive": AUTOMATA_DIR / "nka_recursive.py"
    }


if __name__ == "__main__":

    """GENERATE ALL TYPES OF FSA AND IMPLEMENTATION FROM REGEX"""
    # test_regex = "YYY|{4|Y}"
    # print(f"Generating FSA for regex: {test_regex}")
    # fsa_files = generate_fsa(test_regex)
    # print(f"FSA files generated!")
    #
    # print(f"\nGenerating automata implementations for regex: {test_regex}")
    # automata_files = generate_automata(test_regex)
    # print(f"Automata implementation files generated!")

    """GENERATE RANDOM REGEXES"""

    COUNT = 10

    for regex in generate_assignment_regexes(count=COUNT, min_states=REGEX_MIN_STATES_COUNT, max_states=REGEX_MAX_STATES_COUNT):
        automaton = build_DKA(get_ast_from_regex(regex), regex)
        print(f"{regex:<30} ->  {len(automaton.name_map)} states")