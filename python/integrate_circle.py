import math

sum = 0
r = 1
steps = 10000000


def f(x, r):
    return math.sqrt(r**2 - x**2)


for i in range(steps):
    x = i / steps
    area = f(x, r) * 1 / steps
    sum += area
pi = sum * 4
error = (math.pi - pi) / math.pi
print(pi)
print(steps)
print(math.pi - pi)
print(error * 100, "%")
