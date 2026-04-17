from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

BLOCK_SIZE = 16

def pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def encrypt_ecb(plaintext: str, key: bytes = None):
    if key is None:
        key = os.urandom(16)
    
    padded = pad(plaintext.encode())
    blocks = [padded[i:i+BLOCK_SIZE] for i in range(0, len(padded), BLOCK_SIZE)]
    
    steps = []
    ciphertext_blocks = []

    for i, block in enumerate(blocks):
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        ct_block = encryptor.update(block) + encryptor.finalize()
        ciphertext_blocks.append(ct_block)
        steps.append({
            "block_index": i,
            "plaintext_block": block.hex(),
            "ciphertext_block": ct_block.hex(),
            "identical_to": None  # filled in below
        })

    # Mark duplicate ciphertext blocks (the core ECB flaw)
    seen = {}
    for step in steps:
        ct = step["ciphertext_block"]
        if ct in seen:
            step["identical_to"] = seen[ct]
        else:
            seen[ct] = step["block_index"]

    return {
        "mode": "ECB",
        "key": key.hex(),
        "ciphertext": b"".join(ciphertext_blocks).hex(),
        "steps": steps
    }