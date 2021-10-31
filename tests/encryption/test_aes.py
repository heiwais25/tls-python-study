import random

from tls.encryption.aes import Aes


def test_rotate_inv_rotate_same_result():
    messages = [i for i in range(16)]
    target_message = messages[:]
    aes = Aes()
    aes.rotate(target_message)
    aes.inv_rotate(target_message)
    assert target_message == messages


def test_substitution_and_inverse_same_result():
    messages = [random.randrange(0, 256) for i in range(16)]
    target_message = messages[:]
    aes = Aes()
    aes.substitute(target_message)
    aes.inv_substitute(target_message)
    assert target_message == messages
