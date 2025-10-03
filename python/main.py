import math
import matplotlib.pyplot as plt
import numpy as np

n = int(input("n: "))

def digits(n):
   return len(str(n))

def kaprekar(q):
    d = digits(q)
    if d % 2 == 0:
        k = d / 2
        D = 10 ** k
        x = q % D
        y = q // D
        if q == (x + y) ** 2:
            return True
        return False
    return False

def kaprekars(n):
    k_numbers = []
    s = 1
    while len(k_numbers) < n:
        q = s*s
        if kaprekar(q):
            k_numbers.append(q)
        s += 1
    return k_numbers

plt.style.use('Solarize_Light2')

y = kaprekars(n)
x = range(len(y))

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_yscale('log')
plt.show()
