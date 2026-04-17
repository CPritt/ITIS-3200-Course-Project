from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

BLOCK_SIZE = 16

def pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def encrypt_cbc(plaintext: str, key: bytes = None, iv: bytes = None):
    if key is None:
        key = os.urandom(16)
    if iv is None:
        iv = os.urandom(16)

    padded = pad(plaintext.encode())
    blocks = [padded[i:i+BLOCK_SIZE] for i in range(0, len(padded), BLOCK_SIZE)]

    steps = []
    ciphertext_blocks = []
    prev_block = iv

    for i, block in enumerate(blocks):
        xored = xor_bytes(block, prev_block)
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        ct_block = encryptor.update(xored) + encryptor.finalize()
        ciphertext_blocks.append(ct_block)
        steps.append({
            "block_index": i,
            "plaintext_block": block.hex(),
            "xor_with": prev_block.hex(),   # IV for first block, prev CT after
            "xored_block": xored.hex(),
            "ciphertext_block": ct_block.hex()
        })
        prev_block = ct_block

    return {
        "mode": "CBC",
        "key": key.hex(),
        "iv": iv.hex(),
        "ciphertext": b"".join(ciphertext_blocks).hex(),
        "steps": steps
    }

def decrypt_cbc(ciphertext_hex: str, key_hex: str, iv_hex: str):
    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)
    ciphertext = bytes.fromhex(ciphertext_hex)
    
    blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    prev_block = iv
    plaintext = b""

    for block in blocks:
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(block) + decryptor.finalize()
        plaintext += xor_bytes(decrypted, prev_block)
        prev_block = block

    # Strip padding
    pad_len = plaintext[-1]
    return plaintext[:-pad_len].decode(errors="replace")