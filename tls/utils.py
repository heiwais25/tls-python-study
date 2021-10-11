import random

import gmpy2


def next_prime(n):
    return gmpy2.next_prime(n)


def powm(base, exp, mod):
    return gmpy2.powmod(base, exp, mod)


def byte2mpz(byte_arr):
    return gmpy2.mpz("0x" + "".join(byte_arr))


def random_prime(num_bytes):
    """
    Return the random prime number that has num_bytes length

    :param num_bytes: length of random prime number
    :return: generated random primenumber
    """

    random_bytes = []
    max_bytes = []
    for i in range(num_bytes):
        random_bytes.append(("0x%0.2X" % (random.randint(0, 255)))[2:])
        max_bytes.append("FF")

    new_random_prime = next_prime(byte2mpz(random_bytes))
    max_value = byte2mpz(max_bytes)

    if max_value < new_random_prime:
        return random_prime(num_bytes)

    return new_random_prime
