import math


def turn(current, string, zeros):
    direction = string[:1]
    length = int(string[1:])
    zeros += math.floor(length / 100)

    if direction == "R":
        current = (current + length) % 100
        if str(current) == "0":
            return current, zeros + 1

    if direction == "L":
        current = (current - length) % 100
        if str(current) == "0":
            return current, zeros + 1

    return current, zeros


with open("input1", "r") as file:
    current = 50
    zeros = 0
    for line in file:
        string = line.strip()
        current, zeros = turn(current, string, zeros)
        print(string)
        print(current)
        print("number of zeros: ", zeros)

    print("the password is: ", zeros)
