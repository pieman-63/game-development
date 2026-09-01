import random
from scores import save_score


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
