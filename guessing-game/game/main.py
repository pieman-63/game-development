from game import game
from leaderboard import board, player_history


def menu():
    print("""What would you like to do?
1. Play the game.
2. Access leaderboard.
3. Access player history.""")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        game()
        board()

    elif choice == 2:
        board()

    elif choice == 3:
        player_history()

    else:
        print("Invalid choice.")


menu()
