def turn(current, string):
    direction = string[:1]
    length = int(string[1:])

    if direction == "R":
        current = current + length

    if direction == "L":
        current = current - length

    return current


with open("input", "r") as file:
    current = 50
    zeros = 0
    for line in file:
        print("current: ", current)
        string = line.strip()
        current = turn(current, string)
        print("input: ", string)
        print("zeros: ", zeros)

        if str(current) == "0":
            zeros += 1
            print("[add] exactly zero")

        while current > 99:
            print("[add]", current, " is over 99")
            current -= 100
            zeros += 1

        while current < 0:
            print("[add]", current, " is under 0")
            current += 100
            zeros += 1

        print()

    print("the password is: ", zeros)
