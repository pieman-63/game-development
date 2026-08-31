from challenge import generate_challenge
from scoring import calculate_score
from input_handler import get_guess


def classic_mode(pi, difficulty):
    print("\n" + "-" * 60)
    print("CLASSIC MODE")
    print("-" * 60)

    number, correct_position, length = generate_challenge(
        pi,
        difficulty,
    )

    print(f"\nYour number: {number}")
    print(f"Number length: {length} digits")

    guess = get_guess()

    score, accuracy, difference = calculate_score(
        guess,
        correct_position,
        length,
        difficulty,
        len(pi),
    )

    print("\n" + "-" * 60)

    if guess == correct_position:
        print("PERFECT GUESS!")
    elif guess < correct_position:
        print("Your guess was too low.")
    else:
        print("Your guess was too high.")

    print(f"\nCorrect position : {correct_position:,}")
    print(f"Your guess       : {guess:,}")
    print(f"Difference       : {difference:,}")
    print(f"Accuracy         : {accuracy * 100:.2f}%")
    print(f"Score            : {score:,}")

    print("-" * 60)


def streak_mode(pi, difficulty):
    print("\n" + "-" * 60)
    print("STREAK MODE")
    print("-" * 60)

    streak = 0
    total_score = 0
    valid_guesses = 0

    threshold = difficulty["streak_threshold"]

    print(
        f"\nRequired accuracy to continue: "
        f"{threshold * 100:.0f}%"
    )

    while True:
        number, correct_position, length = generate_challenge(
            pi,
            difficulty,
        )

        print("\n" + "-" * 60)
        print(f"Current streak: {streak}")
        print(f"Number: {number}")

        guess = get_guess()
        valid_guesses += 1

        score, accuracy, difference = calculate_score(
            guess,
            correct_position,
            length,
            difficulty,
            len(pi),
            streak,
        )

        print(f"\nCorrect position: {correct_position:,}")
        print(f"Your guess:       {guess:,}")
        print(f"Difference:       {difference:,}")
        print(f"Accuracy:         {accuracy * 100:.2f}%")

        if accuracy >= threshold:
            streak += 1
            total_score += score

            if guess == correct_position:
                print("\nPERFECT!")
            else:
                print("\nCLOSE ENOUGH!")

            print(f"Streak increased to {streak}!")
            print(f"+{score:,} points")

        else:
            print("\nStreak broken!")

            print(f"\nFinal streak: {streak}")
            print(f"Valid guesses: {valid_guesses}")
            print(f"Total score: {total_score:,}")

            break


def attempts_mode(pi, difficulty):
    print("\n" + "-" * 60)
    print("ATTEMPTS MODE")
    print("-" * 60)

    number, correct_position, length = generate_challenge(
        pi,
        difficulty,
    )

    attempts = 3

    print(f"\nYour number: {number}")
    print(f"You have {attempts} attempts.")
    print("No positional hints will be given.")

    total_score = 0
    valid_guesses = 0

    for attempt in range(1, attempts + 1):
        print(f"\nAttempt {attempt}/{attempts}")

        guess = get_guess()
        valid_guesses += 1

        score, accuracy, difference = calculate_score(
            guess,
            correct_position,
            length,
            difficulty,
            len(pi),
        )

        total_score += score

        if guess == correct_position:
            print("\nCORRECT!")
            print(f"Position: {correct_position:,}")
            print(f"Valid guesses: {valid_guesses}")
            print(f"Score: {total_score:,}")
            return

        remaining = attempts - attempt

        if remaining > 0:
            print("Incorrect.")
            print(f"{remaining} attempt(s) remaining.")

    print("\nOut of attempts!")
    print(f"The correct position was {correct_position:,}.")
    print(f"Valid guesses: {valid_guesses}")
    print(f"Score: {total_score:,}")
