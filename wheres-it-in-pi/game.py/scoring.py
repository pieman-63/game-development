def calculate_score(
    guess,
    correct_position,
    number_length,
    difficulty,
    pi_length,
    streak=0,
):
    """
    Calculate score using absolute positional distance.

    The same distance error receives the same penalty
    regardless of where the correct position is.
    """

    difference = abs(guess - correct_position)

    tolerance_distance = (
        pi_length * difficulty["tolerance"]
    )

    accuracy = max(
        0.0,
        1.0 - difference / (tolerance_distance * 2),
    )

    length_multiplier = 1 + (
        number_length - 1
    ) * 0.15

    streak_multiplier = 1 + min(streak, 10) * 0.05

    base_score = 1000

    score = (
        base_score
        * accuracy
        * length_multiplier
        * difficulty["multiplier"]
        * streak_multiplier
    )

    return max(0, round(score)), accuracy, difference
