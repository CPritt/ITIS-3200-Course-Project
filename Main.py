import os ##for random generation
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding ## for ECB mode padding


def AES_CTR_mode():
    print("AES CTR mode")
    plaintext = input("Enter plaintext: \n").encode()  # Convert plaintext to bytes

    key = os.urandom(16)  # Generate a random 16-byte key
    nonce = os.urandom(8)  # Generate a random 8-byte nonce

    ##----------Setup for AES CTR mode-------
    print("\n-------Setup for AES CTR mode-------")
    print("plaintext:", plaintext.decode())
    print(f"Generated Key: {key.hex()}")
    print(f"Generated Nonce: {nonce.hex()}")
    print("The nonce and counter are each 8 bytes, forming a 16-byte block fed into AES.")

    ##----------Splitting plaintext into blocks-------
    print("\n-------Step 1: Split Plaintext into Blocks-------")
    blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
    print(f"Plaintext split into {len(blocks)} block(s) of up to 16 bytes each.")

    print("\n-------Step 2: Encryption-------")
    print("For each block, a unique counter block is built from the nonce")
    print("and the block number. AES encrypts the counter block to produce")
    print("a keystream, which is then XORed with the plaintext block.")
    print("This repeats for every block, with the counter incrementing each time.")

    ## encryption code from Claude
    ciphertext_blocks = []
    for i, block in enumerate(blocks):
        counter_bytes = i.to_bytes(8, byteorder='big')
        counter_block = nonce + counter_bytes
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        keystream = encryptor.update(counter_block) + encryptor.finalize()
        ct_block = bytes(a ^ b for a, b in zip(block, keystream))
        ciphertext_blocks.append(ct_block)

    ciphertext = b"".join(ciphertext_blocks)

    print(f"\n  Ciphertext : {ciphertext.hex()}")


    ##----------Decryption------- using claude
    input("\nPress Enter to step through decryption...")

    print("\n-------Step 3: Decryption-------")
    print("CTR decryption is identical to encryption.")
    print("We regenerate the same keystream and XOR with the ciphertext.")
    print()

    ct_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    recovered = []
    for i, block in enumerate(ct_blocks):
        counter_bytes = i.to_bytes(8, byteorder='big')
        counter_block = nonce + counter_bytes
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        keystream = encryptor.update(counter_block) + encryptor.finalize()
        pt_block = bytes(a ^ b for a, b in zip(block, keystream))
        recovered.append(pt_block)

    plaintext_recovered = b"".join(recovered).decode(errors='replace')

    print(f"Key                 : {key.hex()}")
    print(f"Nonce               : {nonce.hex()}")
    print(f"Ciphertext          : {ciphertext.hex()}")
    print(f"Recovered Plaintext : {plaintext_recovered}")

    ##----------Vulnerability-------
    input("\nPress Enter to see the nonce reuse vulnerability...")

    print("\n-------Step 4: Vulnerability - Nonce Reuse-------")
    print("If the same key AND nonce encrypt two messages,")
    print("XORing the ciphertexts cancels the keystream entirely.")
    print("C1 XOR C2 = P1 XOR P2  (keystream disappears)")
    print()

    msg2 = input("  Enter a second message to demonstrate: ").encode()
    ct2_blocks = []
    for i, block in enumerate([msg2[j:j+16] for j in range(0, len(msg2), 16)]):
        counter_bytes = i.to_bytes(8, byteorder='big')
        counter_block = nonce + counter_bytes
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        keystream = encryptor.update(counter_block) + encryptor.finalize()
        ct2_blocks.append(bytes(a ^ b for a, b in zip(block, keystream)))

    ciphertext2 = b"".join(ct2_blocks)
    min_len = min(len(ciphertext), len(ciphertext2))
    xored = bytes(a ^ b for a, b in zip(ciphertext[:min_len], ciphertext2[:min_len]))
    p1_xor_p2 = bytes(a ^ b for a, b in zip(plaintext[:min_len], msg2[:min_len]))

    print(f"\nC1        : {ciphertext[:min_len].hex()}")
    print(f"C2        : {ciphertext2[:min_len].hex()}")
    print(f"C1 XOR C2 : {xored.hex()}")
    print(f"P1 XOR P2 : {p1_xor_p2.hex()}")
    print(f"\nNotice C1 XOR C2 equals P1 XOR P2 exactly.")
    print("An attacker who knows one plaintext can recover the other")
    print("without ever knowing the key.")

    ##----------Fix-------
    print("\n-------Fix-------")
    print("Always generate a fresh random nonce for every encryption.")
    print("Never reuse a (key, nonce) pair under any circumstances.")

    input("\nPress Enter to return to the menu...")

def AES_ECB_mode():
    print("AES ECB mode")
    plaintext = input("Enter plaintext: ").encode()

    key = os.urandom(16)  # Generate a random 16-byte key


    ##----------Setup-------
    print("\n-------AES ECB Encryption-------")
    print(f"Plaintext : {plaintext.decode()}")
    print(f"Key       : {key.hex()}")
    print("\nInputs: plaintext, 16-byte key")
    print("ECB encrypts each 16-byte block independently with the same key.")
    print("There is no IV or chaining.")
 
    ##----------Encryption-------
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()
    blocks = [padded[i:i+16] for i in range(0, len(padded), 16)]
 
    ciphertext_blocks = []
    for block in blocks:
        enc = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).encryptor()
        ciphertext_blocks.append(enc.update(block) + enc.finalize())
 
    ciphertext = b"".join(ciphertext_blocks)
    print(f"\nCiphertext : {ciphertext.hex()}")
 
    ##----------Decryption-------
    input("\nPress Enter to see decryption...")
 
    print("\n-------Decryption-------")
    print("Each ciphertext block is decrypted independently with the same key.")
 
    recovered_blocks = []
    for block in ciphertext_blocks:
        dec = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).decryptor()
        recovered_blocks.append(dec.update(block) + dec.finalize())
 
    unpadder = padding.PKCS7(128).unpadder()
    plaintext_recovered = unpadder.update(b"".join(recovered_blocks)) + unpadder.finalize()
    print(f"\nRecovered Plaintext : {plaintext_recovered.decode(errors='replace')}")
 
    ##----------Vulnerability-------
    input("\nPress Enter to see the ECB pattern vulnerability...")
 
    print("\n-------Vulnerability - Pattern Leakage-------")
    print("Identical plaintext blocks always produce identical ciphertext blocks.")
    print("An attacker can detect repeated data without ever breaking the key.")
    print()
 
    repeat_msg = (plaintext * 3)[:48]
    padder2 = padding.PKCS7(128).padder()
    repeat_padded = padder2.update(repeat_msg) + padder2.finalize()
    repeat_blocks = [repeat_padded[i:i+16] for i in range(0, len(repeat_padded), 16)]
 
    repeat_ct_blocks = []
    for block in repeat_blocks:
        enc = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend()).encryptor()
        repeat_ct_blocks.append(enc.update(block) + enc.finalize())
 
    print(f"Repeating plaintext : {repeat_msg.decode(errors='replace')}")
    print("Ciphertext blocks:")
    for i, (pb, cb) in enumerate(zip(repeat_blocks, repeat_ct_blocks)):
        marker = " <-- DUPLICATE" if repeat_ct_blocks.count(cb) > 1 else ""
        print(f"  Block {i}: {cb.hex()}{marker}")
 
    print("\nDuplicate plaintext blocks produce duplicate ciphertext blocks,")
    print("leaking the structure of the data to any observer.")
 
    ##----------Fix-------
    print("\n-------Fix-------")
    print("Never use ECB mode for encrypting more than one block of sensitive data.")
    print("Use CBC with a random IV, or CTR with a unique nonce instead.")
 
    input("\nPress Enter to return to the menu...")



def AES_CBC_mode_fixed_IV():
    print("AES CBC mode (Fixed IV)")
    plaintext = input("Enter plaintext: ").encode()

def AES_CBC_mode_random_IV_HMAC():
    print("AES CBC mode (Random IV) + HMAC")
    plaintext = input("Enter plaintext: ").encode()


def main():
    print("===========Course Project===========")
    while True:
        print("\n[1] AES CTR mode")
        print("[2] AES ECB mode")
        print("[3] AES CBC mode (Fixed IV)")
        print("[4] AES CBC mode (Random IV) + HMAC")
        print("[q] Quit")
        choice = input("\n> ").strip().lower()

        if choice == "1":
            AES_CTR_mode()
        elif choice == "2":
            AES_ECB_mode()
        elif choice == "3":
            AES_CBC_mode_fixed_IV()
        elif choice == "4":
            AES_CBC_mode_random_IV_HMAC()
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
