from pi_manager import load_pi
from display import print_header, print_guidelines
from input_handler import choose_difficulty
from modes import (
    classic_mode,
    streak_mode,
    attempts_mode,
)


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


if __name__ == "__main__":
    main()
