import random
import os
from decimal import Decimal, getcontext


# ============================================================
# CONFIGURATION
# ============================================================

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


# ============================================================
# PI GENERATION
# ============================================================

def generate_pi(digits):
    """
    Generate pi to the requested number of digits.

    Position 1 = 3
    Position 2 = 1
    Position 3 = 4
    """

    getcontext().prec = digits + 10

    C = 426880 * Decimal(10005).sqrt()

    M = 1
    L = 13591409
    X = 1
    K = 6
    S = Decimal(L)

    terms = digits // 14 + 2

    for i in range(1, terms):
        M = (K**3 - 16 * K) * M // (i**3)
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / Decimal(X)
        K += 12

    pi = C / S

    return str(pi).replace(".", "")[:digits]


def load_pi():
    """Load stored pi or generate it if necessary."""

    if os.path.exists(PI_FILE):
        print(f"Loading pi from {PI_FILE}...")

        try:
            with open(PI_FILE, "r", encoding="utf-8") as file:
                pi = file.read().strip()

            if (
                len(pi) == PI_DIGITS
                and pi.isdigit()
                and pi.startswith("314")
            ):
                print("Pi loaded!")
                return pi

            print("Stored pi file is invalid or has the wrong length.")

        except OSError:
            print("Could not read the stored pi file.")

    print(f"Generating the first {PI_DIGITS:,} digits of pi...")

    pi = generate_pi(PI_DIGITS)

    try:
        with open(PI_FILE, "w", encoding="utf-8") as file:
            file.write(pi)

        print(f"Pi generated and saved to {PI_FILE}!")

    except OSError:
        print("Pi generated, but could not save the file.")

    return pi


# ============================================================
# CHALLENGE GENERATION
# ============================================================

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


# ============================================================
# SCORING
# ============================================================

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

    tolerance_distance = pi_length * difficulty["tolerance"]

    # Accuracy decreases linearly with absolute distance.
    accuracy = max(
        0.0,
        1.0 - difference / (tolerance_distance * 2),
    )

    length_multiplier = 1 + (number_length - 1) * 0.15

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


# ============================================================
# DISPLAY
# ============================================================

def print_header():
    print()
    print("=" * 60)
    print("                 WHERE'S IT IN PI?")
    print("=" * 60)
    print()


def print_guidelines():
    print("\n" + "=" * 60)
    print("GUIDELINES")
    print("=" * 60)

    print(f"""
1. The game uses the first {PI_DIGITS:,} digits of pi.

2. The digits begin with:

       314159265358979...

   Therefore:

       Position 1 = 3
       Position 2 = 1
       Position 3 = 4
       Position 4 = 1

3. You will be shown a sequence of digits from pi.

4. Your goal is to guess where that sequence FIRST appears.

5. Position counting starts at 1, not 0.

6. Accuracy is based on absolute distance.

   Being 100 positions away is equally inaccurate
   anywhere in the range.

7. Each difficulty changes:
   - Number length
   - Accuracy tolerance
   - Score multiplier
   - Streak requirements

8. Classic Mode gives you one challenge.

9. Streak Mode continues if your accuracy meets
   the required threshold.

10. Attempts Mode gives you three guesses.

    No hints are given between attempts.

11. Pi is stored locally after generation.
""")

    print("=" * 60)


# ============================================================
# DIFFICULTY
# ============================================================

def choose_difficulty():
    print("\nChoose difficulty:\n")

    for key, difficulty in DIFFICULTIES.items():
        print(
            f"  {key}. {difficulty['name']} "
            f"({difficulty['min_length']}-"
            f"{difficulty['max_length']} digits)"
        )

    print()

    while True:
        choice = input("Choice: ").strip()

        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]

        print("Please choose a valid difficulty.")


# ============================================================
# INPUT
# ============================================================

def get_guess():
    """Get a valid position guess."""

    while True:
        try:
            guess = int(
                input("\nYour position guess: ")
                .replace(",", "")
                .strip()
            )

            if 1 <= guess <= PI_DIGITS:
                return guess

            print(
                f"Enter a number between 1 and {PI_DIGITS:,}."
            )

        except ValueError:
            print("Please enter a whole number.")


# ============================================================
# CLASSIC MODE
# ============================================================

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


# ============================================================
# STREAK MODE
# ============================================================

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


# ============================================================
# ATTEMPTS MODE
# ============================================================

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


# ============================================================
# MAIN MENU
# ============================================================

def main():
    print_header()

    pi = load_pi()

    while True:
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)

        print("""
1. Classic
2. Streak
3. Attempts
4. Guidelines
5. Exit
""")

        mode = input("Choose a mode: ").strip()

        if mode == "5":
            print("\nThanks for playing!")
            break

        if mode == "4":
            print_guidelines()
            input("\nPress ENTER to return to the menu...")
            continue

        if mode not in {"1", "2", "3"}:
            print("Invalid choice.")
            continue

        difficulty = choose_difficulty()

        if mode == "1":
            classic_mode(pi, difficulty)

        elif mode == "2":
            streak_mode(pi, difficulty)

        elif mode == "3":
            attempts_mode(pi, difficulty)

        input("\nPress ENTER to return to the menu...")


# ============================================================
# START GAME
# ============================================================

if __name__ == "__main__":
    main()
