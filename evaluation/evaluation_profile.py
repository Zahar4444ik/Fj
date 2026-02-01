EVALUATION_PROFILE = {

    "global": {
        "total_score": 100,

        "test_words": {
            "count": 20,
            "bad_word_ratio_level": 2
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
