import math

import matplotlib.pyplot as plt


def check1(a, b, c):
    return a + b + c


def check2(a, b, c):
    return a * b + b * c + a * c


def check3(a, b, c):
    return a**2 + b**2 + c**2


def divides(p, q):
    if p == 0:
        return False
    return q % p == 0


def is_prime(p):
    if p <= 1:
        return False
    else:
        is_prime = True  # Flag variable
        for i in range(2, int(p**0.5) + 1):
            if p % i == 0:
                is_prime = False
                break
        return is_prime


def primes_up_to(n):
    """Return a list of all primes ≤ n using a sieve."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    p = 2
    while p * p <= n:
        if sieve[p]:
            for multiple in range(p * p, n + 1, p):
                sieve[multiple] = False
        p += 1
    return [i for i, is_prime in enumerate(sieve) if is_prime]


upper_bound = 150
divisions = []

for a in range(1, upper_bound):
    for b in range(1, upper_bound):
        if b >= a:
            for c in range(1, upper_bound):
                if c >= b:
                    A = check1(a, b, c)
                    B = check2(a, b, c)
                    C = A**2 - 2 * B

                    if is_prime(A):
                        # print("triple", a, b, c)
                        # print(check1(a, b, c), "is prime")

                        # print(check2(a, b, c), "is ab + bc + ca")
                        # print(check3(a, b, c), "is a^2 + b^2 + c^2")
                        # print("division ", check3(a, b, c) / check2(a, b, c))
                        divisions.append((C % B))

                        if divides(check2(a, b, c), check3(a, b, c)):
                            print(a, b, c, "matches the condition")
                        # print()
# print(divisions)


primes = primes_up_to(len(divisions) - 1)

# for p in primes:
# plt.axvline(x=p, linestyle="--", linewidth=0.5)

plt.plot(divisions)  # line graph, x = 0,1,2,...
plt.xlabel("Index")
plt.ylabel("Division")

plt.yscale("log")
plt.show()
