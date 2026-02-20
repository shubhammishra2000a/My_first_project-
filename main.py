"""
Main entry point.
Lets the user choose between the Schedule Handler app and the Notepad app.
"""

import schedule_handler
import notepad


def main():
    print("=== My First Project ===")
    print("1. Schedule Handler")
    print("2. Notepad")
    print("3. Exit")
    choice = input("Choose an app: ").strip()
    if choice == "1":
        schedule_handler.run()
    elif choice == "2":
        notepad.run()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
