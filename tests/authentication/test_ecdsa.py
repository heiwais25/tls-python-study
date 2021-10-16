from gmpy2 import mpz

from tls.authentication.ecdsa import Ecdsa
from tls.keyexchange.ec import EcField, EcPoint
from tls.utils import random_prime


def test_sign_verify_message_by_secp256r1():
    field = EcField(
        mpz("0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc"),
        mpz("0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b"),
        mpz("0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff")
    )

    generator_point = EcPoint(
        mpz("0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296"),
        mpz("0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"),
        field
    )

    n = mpz("0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551")
    d = random_prime(31)
    q = d * generator_point

    ecdsa = Ecdsa(generator_point, n)

    message = "Hello This is ECDSA authentication"
    h = mpz(hash(message))
    signatures = ecdsa.sign(h, d)
    assert ecdsa.verify(h, signatures, q)
