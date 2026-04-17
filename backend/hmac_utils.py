import hmac
import hashlib

def generate_tag(key: bytes, ciphertext_hex: str) -> str:
    tag = hmac.new(key, bytes.fromhex(ciphertext_hex), hashlib.sha256).hexdigest()
    return tag

def verify_tag(key: bytes, ciphertext_hex: str, tag: str) -> bool:
    expected = hmac.new(key, bytes.fromhex(ciphertext_hex), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, tag)