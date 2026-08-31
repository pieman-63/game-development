PI_DIGITS = 10_000
PI_FILE = "pi_digits.txt"


DIFFICULTIES = {
    "1": {
        "name": "Easy",
        "min_length": 1,
        "max_length": 3,
        "tolerance": 0.10,
        "multiplier": 1.0,
        "streak_threshold": 0.60,
    },
    "2": {
        "name": "Medium",
        "min_length": 4,
        "max_length": 6,
        "tolerance": 0.05,
        "multiplier": 1.5,
        "streak_threshold": 0.70,
    },
    "3": {
        "name": "Hard",
        "min_length": 7,
        "max_length": 10,
        "tolerance": 0.02,
        "multiplier": 2.5,
        "streak_threshold": 0.80,
    },
    "4": {
        "name": "Insane",
        "min_length": 11,
        "max_length": 20,
        "tolerance": 0.01,
        "multiplier": 5.0,
        "streak_threshold": 0.90,
    },
}
