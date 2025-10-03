def function(n):
    return (2 * 10**n - 0.2) / 1.9


i = False
n = 1
while i is False:
    if function(n) % 1 == 0:
        print(n)
        print(int(function(n)))
        i = True
    n += 1
