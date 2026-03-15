"""
Configuration parser for FSA assignments lifecycle

This module loads and parses environment variables from .env file..
"""

import os
from dotenv import load_dotenv

load_dotenv()


# -------------------------------------------------------------------------------
# QUESTION GENERATION
# -------------------------------------------------------------------------------

CATEGORY = os.getenv("QUIZ_CATEGORY", "default")

NUMBER_OF_QUESTIONS = int(os.getenv("NUMBER_OF_QUESTIONS", "0"))

REGEX_MIN_STATES_COUNT = int(os.getenv("REGEX_MIN_STATES_COUNT", "1"))
REGEX_MAX_STATES_COUNT = int(os.getenv("REGEX_MAX_STATES_COUNT", "1"))

AUTOMATON_TYPE = os.getenv("AUTOMATON_TYPE", "")

IMPLEMENTATION_TYPE = os.getenv("IMPLEMENTATION_TYPE", "")

MAX_ALPHABET_SIZE = int(os.getenv("MAX_ALPHABET_SIZE", "0"))
MIN_ALPHABET_SIZE = int(os.getenv("MIN_ALPHABET_SIZE", "0"))

# -------------------------------------------------------------------------------
# QUESTION PROPERTIES & EVALUATION SETTINGS
# -------------------------------------------------------------------------------

TITLE = os.getenv("REPORT_TITLE", "Unnamed Test")

ASSIGNMENT_MAX_POINTS = int(os.getenv("ASSIGNMENT_MAX_POINTS", "0"))

TEST_WORDS_COUNT = int(os.getenv("TEST_WORDS_COUNT", "0"))

BAD_WORD_RATIO_LEVEL = float(os.getenv("BAD_WORD_RATIO_LEVEL", "0.0"))

GROUP_SIZE = int(os.getenv("GROUP_SIZE", "0"))

# System constant
TOTAL_SCORE = 100

DKA_FSA_ISOMORPHISM = int(os.getenv("DKA_FSA_ISOMORPHISM", "0"))
DKA_FSA_ANNOTATIONS = int(os.getenv("DKA_FSA_ANNOTATIONS", "0"))
DKA_FSA_TOTAL = DKA_FSA_ANNOTATIONS + DKA_FSA_ISOMORPHISM
DKA_IMPLEMENTATION = int(os.getenv("DKA_IMPLEMENTATION", "0"))

NKA_FSA_ISOMORPHISM = int(os.getenv("NKA_FSA_ISOMORPHISM", "0"))
NKA_IMPLEMENTATION = int(os.getenv("NKA_IMPLEMENTATION", "0"))


# -------------------------------------------------------------------------------
# MOODLE AUTHENTICATION & FILE OPERATIONS
# -------------------------------------------------------------------------------

# Credentials
USERNAME = os.getenv("MOODLE_USERNAME", "")
PASSWORD = os.getenv("MOODLE_PASSWORD", "")

# Moodle resources
ASSIGNMENT_LINK = os.getenv("ASSIGNMENT_LINK", "")

QUESTION_NUMBER = int(os.getenv("QUESTION_NUMBER", "1"))
