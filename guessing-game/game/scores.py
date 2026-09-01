import csv


def save_score(name, total_attempts, average):
    with open("scores.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, total_attempts, average])


def read_scores():
    scores = []

    try:
        with open("scores.csv", "r", newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                participant = row[0]
                total = int(row[1])
                average_score = float(row[2])

                scores.append(
                    (participant, total, average_score)
                )

    except FileNotFoundError:
        pass

    return scores
