# Project: Task Manager CLI

# File: main.py

def main():
    print("Welcome to the Task Manager CLI!")
    print("Choose an option:")
    print("1. View tasks")
    print("2. Add a task")
    print("3. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        view_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
