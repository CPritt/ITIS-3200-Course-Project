import os ##for random generation


def AES_CTR_mode():
    print("AES CTR mode")
    plaintext = input("Enter plaintext: \n")

    key = os.urandom(16)  # Generate a random 16-byte key
    nonce = os.urandom(8)  # Generate a random 8-byte nonce

    ##----------Setup for AES CTR mode-------
    print("\n-------Setup for AES CTR mode-------")
    print("plaintext:", plaintext)
    print(f"Generated Key: {key.hex()}")
    print(f"Generated Nonce: {nonce.hex()}")
    print("Using 8-byte nonce and 8-byte counter for AES CTR mode.")


def AES_ECB_mode():
    print("AES ECB mode")
    plaintext = input("Enter plaintext: ")

def AES_CBC_mode_fixed_IV():
    print("AES CBC mode (Fixed IV)")
    plaintext = input("Enter plaintext: ")

def AES_CBC_mode_random_IV_HMAC():
    print("AES CBC mode (Random IV) + HMAC")
    plaintext = input("Enter plaintext: ")


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
