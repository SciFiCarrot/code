import math
import time
import matplotlib.pyplot as plt
import numpy as np


def is_kaprekar(n: int) -> bool:
    """Return ``True`` if ``n`` is a Kaprekar number."""
    if n < 1:
        return False
    sq = n * n
    div = 10
    while div <= sq:
        left, right = divmod(sq, div)
        if right and left + right == n:
            return True
        div *= 10
    return False


def find_kaprekars(limit: int) -> np.ndarray:
    """Return an array of all Kaprekar numbers up to ``limit``."""
    return np.fromiter(
        (i for i in range(1, limit + 1) if is_kaprekar(i)), dtype=int
    )


def main() -> None:
    try:
        limit = int(input("Obergrenze: "))
    except ValueError:
        raise SystemExit("Bitte eine ganze Zahl eingeben.")

    start = time.perf_counter()
    numbers = find_kaprekars(limit)
    elapsed = time.perf_counter() - start
    print(f"{len(numbers)} Kaprekar-Zahlen gefunden in {elapsed:.3f}s")

    plt.style.use("Solarize_Light2")
    fig, ax = plt.subplots()
    ax.plot(np.arange(1, len(numbers) + 1), numbers)
    ax.set_xlabel("Index")
    ax.set_ylabel("Kaprekar-Zahl")
    ax.set_yscale("log")
    plt.show()


if __name__ == "__main__":
    main()
