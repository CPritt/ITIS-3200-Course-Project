from flask import Flask, request, jsonify
from flask_cors import CORS
from ecb import encrypt_ecb
from cbc import encrypt_cbc, decrypt_cbc
from hmac_utils import generate_tag, verify_tag
from attacks.cbc_bitflip import bitflip
import os

app = Flask(__name__)
CORS(app)  # allows React frontend on localhost:3000 to call this

@app.route("/encrypt/ecb", methods=["POST"])
def ecb():
    data = request.get_json()
    plaintext = data.get("plaintext", "")
    result = encrypt_ecb(plaintext)
    return jsonify(result)

@app.route("/encrypt/cbc", methods=["POST"])
def cbc():
    data = request.get_json()
    plaintext = data.get("plaintext", "")
    use_hmac = data.get("hmac", False)
    result = encrypt_cbc(plaintext)
    if use_hmac:
        hmac_key = os.urandom(16)
        result["hmac_tag"] = generate_tag(hmac_key, result["ciphertext"])
        result["hmac_key"] = hmac_key.hex()
    return jsonify(result)

@app.route("/decrypt/cbc", methods=["POST"])
def cbc_decrypt():
    data = request.get_json()
    plaintext = decrypt_cbc(data["ciphertext"], data["key"], data["iv"])
    return jsonify({"plaintext": plaintext})

@app.route("/attack/bitflip", methods=["POST"])
def attack_bitflip():
    data = request.get_json()
    flipped_ct = bitflip(data["ciphertext"], data["byte_position"], data["flip_value"])
    # Decrypt the tampered ciphertext to show the corruption
    corrupted_pt = decrypt_cbc(flipped_ct, data["key"], data["iv"])
    return jsonify({
        "tampered_ciphertext": flipped_ct,
        "corrupted_plaintext": corrupted_pt
    })

@app.route("/verify/hmac", methods=["POST"])
def verify():
    data = request.get_json()
    valid = verify_tag(
        bytes.fromhex(data["hmac_key"]),
        data["ciphertext"],
        data["tag"]
    )
    return jsonify({"valid": valid})

if __name__ == "__main__":
    app.run(debug=True, port=5000)