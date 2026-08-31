from config import PI_DIGITS


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
