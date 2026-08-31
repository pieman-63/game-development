from config import PI_DIGITS, DIFFICULTIES


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
