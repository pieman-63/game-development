import random


def generate_challenge(pi, difficulty):
    """Generate a random sequence from pi."""

    min_length = difficulty["min_length"]
    max_length = difficulty["max_length"]

    length = random.randint(min_length, max_length)
    start = random.randint(0, len(pi) - length)

    number = pi[start:start + length]

    # The first occurrence is the correct answer.
    correct_position = pi.find(number) + 1

    return number, correct_position, length
