import os

def menu():
    print("\n====== FACE AUTHENTICATION SYSTEM ======")
    print("1. Register New User")
    print("2. Start Attendance (Punch In / Out)")
    print("3. Delete User")
    print("4. Exit")
    return input("Choose option (1-4): ")

def main():
    while True:
        choice = menu()

        if choice == "1":
            os.system("python3 src/register_user.py")

        elif choice == "2":
            os.system("python3 src/attendance.py")

        elif choice == "3":
            os.system("python3 src/delete_user.py")

        elif choice == "4":
            print("Exiting system. Bye 👋")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
