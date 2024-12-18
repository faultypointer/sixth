def primes(n):
    primes = []
    for i in range(2, n+1):
        is_prime = True
        for prev in primes:
            if i % prev == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes


if __name__ == "__main__":
    primes_upto_100 = primes(100)
    print("Primes upto 100:\n", primes_upto_100)
