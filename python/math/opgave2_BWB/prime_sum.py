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


primes = primes_up_to(100)


a = 1
b = 1
c = 1


triples_by_prime = {}


for p in primes:
    # if p == 2:
    #   continue

    triples_by_prime[p] = []

    for a in range(1, p - 1):
        for b in range(a, p - a):  # b ≥ a and leave room for c ≥ 1
            c = p - a - b
            if c < b:  # we want c ≥ b
                break  # increasing b only makes c smaller
            triples_by_prime[p].append((a, b, c))

        # print("prime is ", p)
        # print("a is ", a)
        # print("b is ", b)
        # print("c is ", c)

for p, triples in triples_by_prime.items():
    print(p, "has", len(triples), "triples")
