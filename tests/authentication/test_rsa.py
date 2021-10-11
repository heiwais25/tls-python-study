from tls.authentication.rsa import Rsa
from gmpy2 import mpz


def test_rsa_encryption_decryption():
    rsa = Rsa(256)
    original_value = mpz("0x23423423")
    encoded_Value = rsa.encode(original_value)
    assert original_value == rsa.decode(encoded_Value)


def test_rsa_sign_and_encode():
    rsa = Rsa(256)
    certificate_hash = mpz("0x156781f45f8f7f")
    signed_value = rsa.sign(certificate_hash)
    assert certificate_hash == rsa.encode(signed_value)