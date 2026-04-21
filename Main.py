def main():
    print("===========Course Project===========")
    while True:
        print("\n[1] Caesar Cipher")
        print("[2] XOR Cipher")
        print("[q] Quit")
        choice = input("\n> ").strip().lower()

        if choice == "1":
            print("1")
        elif choice == "2":
            print("2")
        elif choice == "q":
            print("3")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

