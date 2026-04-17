def bitflip(ciphertext_hex: str, byte_position: int, flip_value: int) -> str:
    """Flip a single byte in the ciphertext. The corruption propagates
    to the corresponding byte in the NEXT plaintext block on decryption."""
    ct = bytearray(bytes.fromhex(ciphertext_hex))
    if byte_position >= len(ct):
        raise ValueError("Byte position out of range")
    ct[byte_position] ^= flip_value
    return ct.hex()