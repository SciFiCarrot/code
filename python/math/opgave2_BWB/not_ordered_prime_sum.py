import matplotlib as plt

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

triples_by_prime = {}

for p in primes:
    if p == 2:
        continue  # can't write 2 as sum of 3 positive ints

    triples_by_prime[p] = []

    # ordered triples (a, b, c) with a,b,c >= 1 and a + b + c = p
    for a in range(1, p - 1):  # a >= 1
        for b in range(1, p - a):  # b >= 1, leave room for c >= 1
            c = p - a - b  # c is forced by the sum
            if c >= 1:
                triples_by_prime[p].append((a, b, c))

for p, triples in triples_by_prime.items():
    print(p, len(triples), "triples:")
