from scores import read_scores


def board():
    scores = read_scores()

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


def player_history():
    scores = read_scores()

    print("\n========== PLAYER HISTORY ==========")

    for participant, total, average_score in scores:
        print("Player:", participant)
        print("Total attempts:", total)
        print("Average score:", average_score)
        print("-" * 40)
