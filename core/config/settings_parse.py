import os

from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Global
# -----------------------------
CATEGORY = os.getenv("CATEGORY", "default")
TITLE = os.getenv("TITLE", "Unnamed Test")

TEST_WORDS_COUNT = int(os.getenv("TEST_WORDS_COUNT", 0))
BAD_WORD_RATIO_LEVEL = float(os.getenv("BAD_WORD_RATIO_LEVEL", 0))
GROUP_SIZE = int(os.getenv("GROUP_SIZE", 0))

REGEX_MIN_STATES_COUNT = int(os.getenv("REGEX_MIN_STATES_COUNT", 0))
REGEX_MAX_STATES_COUNT = int(os.getenv("REGEX_MAX_STATES_COUNT", 0))

TOTAL_SCORE = 100  # fixed system invariant


# -----------------------------
# DKA
# -----------------------------
DKA_FSA_ISOMORPHISM = int(os.getenv("DKA_FSA_ISOMORPHISM", 0))
DKA_FSA_ANNOTATIONS = int(os.getenv("DKA_FSA_ANNOTATIONS", 0))
DKA_FSA_TOTAL = DKA_FSA_ANNOTATIONS + DKA_FSA_ISOMORPHISM

DKA_IMPLEMENTATION = int(os.getenv("DKA_IMPLEMENTATION", 0))


# -----------------------------
# NKA
# -----------------------------
NKA_FSA_ISOMORPHISM = int(os.getenv("NKA_FSA_ISOMORPHISM", 0))
NKA_IMPLEMENTATION = int(os.getenv("NKA_IMPLEMENTATION", 0))
