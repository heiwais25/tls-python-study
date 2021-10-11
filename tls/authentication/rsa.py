import gmpy2

from tls.utils import random_prime, next_prime


class Rsa:
    def __init__(self, key_size):
        p = random_prime(int(key_size / 2))
        q = random_prime(int(key_size / 2))
        self.K = p * q

        phi = gmpy2.lcm(p - 1, q - 1)
        e = gmpy2.mpz("0x10001")
        while gmpy2.gcd(phi, e) != 1:
            e = next_prime(e)

        self.e = e
        self.d = gmpy2.invert(e, phi)

    def encode(self, value):
        return gmpy2.powmod(value, self.e, self.K)

    def decode(self, encoded_value):
        return gmpy2.powmod(encoded_value, self.d, self.K)

    def sign(self, value):
        return self.decode(value)
