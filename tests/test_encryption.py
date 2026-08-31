from security.encryption import (
    decrypt_data,
    encrypt_data,
)


def test_encrypt_decrypt():
    original = "Sensitive Enterprise EMS Data"

    encrypted = encrypt_data(original)

    assert encrypted != original
    assert decrypt_data(encrypted) == original


def test_different_ciphertext_for_same_value():
    original = "Sensitive Enterprise EMS Data"

    encrypted_1 = encrypt_data(original)
    encrypted_2 = encrypt_data(original)

    assert encrypted_1 != encrypted_2
    assert decrypt_data(encrypted_1) == original
    assert decrypt_data(encrypted_2) == original
