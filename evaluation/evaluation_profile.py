EVALUATION_PROFILE = {

    "global": {
        "total_score": 100,

        "test_words": {
            "count": 20,
            # 0–3 → difficulty / aggressiveness
            "bad_word_ratio_level": 2
            # 0 = 0%
            # 1 = 10%
            # 2 = 20%
            # 3 = 30%
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
            "total": 60,
            "iterative": 60,
            "recursive": 60
        }
    },

    "NKA": {
        "fsa": {
            "total": 30,
            "isomorphism": 30
        },
        "implementation": {
            "total": 70,
            "iterative": 70,
            "recursive": 70
        }
    }
}
