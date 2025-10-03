n = int(input("Obergrenze: "))


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


kaprekars = []

for i in range(n):
    if is_kaprekar(i):
        kaprekars.append(i)

for kaprekar in kaprekars:
    square = kaprekar * kaprekar
    if square % 5 == 0:
        print(str(square)[-2:])
        print(kaprekar % 9)
