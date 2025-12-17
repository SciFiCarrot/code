def is_invalid(id):
    id = str(id)
    id_hlen = int(len(id) / 2)
    id_r = id[id_hlen:]
    id_l = id[:id_hlen]
    if id_l == id_r:
        return True
    return False


with open("input2", "r") as file:
    for line in file:
        ids = line.split(",")


password = 0

for id in ids:
    print(id)

    id = id.strip()
    lb = int(id.split("-")[0].strip())
    ub = int(id.split("-")[1].strip())
    print(lb, ub)
    current_check = lb
    print("current: ", current_check)
    while current_check <= ub:
        if is_invalid(id):
            print(id)
            password += int(id)
            current_check += 1
