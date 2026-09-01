import csv
import random


# =========================================>
# GAME
# =========================================>

def game():
    total_attempts = 0
    name = input("Enter participant name: ")

    for i in range(3):
        attempts = play_round()
        total_attempts += attempts

    average = total_attempts / 3

    print("Your average score is:", average)
    print("Total attempts taken:", total_attempts)

    save_score(name, total_attempts, average)


def play_round():
    attempts = 0
    sec = random.randint(1, 100)

    print("""Number guessing game
===========================================
Guess a number between 1 and 100, both numbers included.""")

    guess = int(input("Enter your guess: "))
    attempts += 1

    while guess != sec:

        if guess < sec - 30:
            print("Your guess is much too low.")

        elif guess > sec + 30:
            print("Your guess is much too high.")

        elif guess < sec:
            print("Not quite. Your guess is low.")

        elif guess > sec:
            print("Not quite. Your guess is high.")

        guess = int(input("Enter your guess: "))
        attempts += 1

    print("You got it right.")
    print("No. of attempts:", attempts)
    print("*" * 50)

    return attempts


# =========================================>
# SAVE PLAYER HISTORY
# =========================================>

def save_score(name, total_attempts, average):
    with open("scores.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, total_attempts, average])


# =========================================>
# READ PLAYER HISTORY
# =========================================>

def read():
    scores = []

    with open("scores.csv", "r", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            participant = row[0]
            total = int(row[1])
            average_score = float(row[2])

            scores.append(
                (participant, total, average_score)
            )

    return scores


# =========================================>
# LEADERBOARD
# =========================================>

def board():
    scores = read()

    leaderboard = sorted(
        scores,
        key=lambda x: x[2]
    )

    print("\n========== LEADERBOARD ==========")

    position = 1

    for participant, total, average_score in leaderboard:
        print(
            position,
            "-",
            participant,
            average_score
        )

        position += 1
# =========================================>
# PLAYER HISTORY
# =========================================>

def player_history():
    scores = read()

    print("\n========== PLAYER HISTORY ==========")

    for participant, total, average_score in scores:
        print("Player:", participant)
        print("Total attempts:", total)
        print("Average score:", average_score)
        print("-" * 40)
# =========================================>
# MENU
# =========================================>

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


# =========================================>
# MAIN PROGRAM
# =========================================>

menu()
