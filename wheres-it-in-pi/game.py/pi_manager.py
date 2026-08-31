import os
from decimal import Decimal, getcontext

from config import PI_DIGITS, PI_FILE


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

