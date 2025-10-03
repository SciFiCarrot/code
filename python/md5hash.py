import hashlib

s = "hacktheweb"
n = 0
status = False
while not status:
    string = s + str(n)
    hash = hashlib.md5(string.encode())
    check_hash = str(hash.hexdigest())[:6]
    print(check_hash)
    if check_hash == "000000":
        print("Found it:", n)
        print(hash.hexdigest())
        status = True
    n += 1
