from tls.keyexchange.ec import EcPoint
from tls.utils import random_prime
from gmpy2 import invert


class Ecdsa:
    def __init__(self, g: EcPoint, n):
        """
        Initialize ECDSA with generator and order of the curve
        """
        self.n = n
        self.g = g
        self.n_bits = n.bit_length()

    def sign(self, message, d):
        z = message >> max(message.bit_length() - self.n_bits, 0)

        while True:
            while True:
                k = random_prime(31)
                p = k * self.g
                r = p.x % self.n
                if r != 0:
                    break
            s = (invert(k, self.n) * (z + r * d)) % self.n
            if s != 0:
                break

        return r, s

    def verify(self, message, signatures, q) -> bool:
        """
        message: signed message
        signatures: (r, s) - arbitrary generated key, signed by private key
        q: Public key - d x G
        """
        r, s = signatures

        m_bits = message.bit_length()
        z = message >> max(m_bits - self.n_bits, 0)
        u1 = (z * invert(s, self.n)) % self.n
        u2 = (r * invert(s, self.n)) % self.n
        p = u1 * self.g + u2 * q
        if p.y == p.f.mod:
            return False

        return (p.x - r) % self.n == 0
