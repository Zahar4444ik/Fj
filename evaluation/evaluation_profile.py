TEST_WORDS_COUNT = 20
BAD_WORD_RATIO_LEVEL = 2
GROUP_SIZE = 5

EVALUATION_PROFILE = {

    "global": {
        "total_score": 100,

        "test_words": {
            "count": 20,
            "bad_word_ratio_level": 2
        },
        "group_testing": {
            "group_size": 5,
        },

        "regex_complexity": {
            "min_depth": 1,
            "max_depth": 3,
        }
    },

    "DKA": {
        "fsa": {
            "total": 40,
            "isomorphism": 30,
            "annotations": 10,
        },
        "implementation": {
            "total": 60
        }
    },

    "NKA": {
        "fsa": {
            "total": 30,
            "isomorphism": 30
        },
        "implementation": {
            "total": 70
        }
    }
}
