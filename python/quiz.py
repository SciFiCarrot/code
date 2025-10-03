def is_special(n):
    string = str(n)
    last = string[-1:]
    new = last + string[:-1]
    if 2 * string == new:
        return True
    return False


for i in range(1000000000000):
    if is_special(i):
        print(i)
