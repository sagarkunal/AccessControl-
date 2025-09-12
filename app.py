import json
import os
import hashlib

USERS_FILE = "users.json"

# Load users from JSON file
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as file:
            data = file.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except json.JSONDecodeError:
        return {}

# Save users to JSON file
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup new user
def signup():
    users = load_users()
    username = input("Enter username: ")
    if username in users:
        print("Username already exists!")
        return
    password = input("Enter password: ")
    role = input("Enter role (admin/user): ").lower()
    if role not in ["admin", "user"]:
        print("Invalid role! Defaulting to 'user'.")
        role = "user"

    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    save_users(users)
    print(f"User '{username}' created successfully!")

# Login existing user
def login():
    users = load_users()
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username]["password"] == hash_password(password):
        role = users[username]["role"]
        print(f"\nLogin successful! Welcome {username} ({role})\n")
        if role == "admin":
            admin_dashboard(username)
        else:
            user_dashboard(username)
    else:
        print("Invalid username or password!")

# Admin dashboard
def admin_dashboard(username):
    print(f"=== Admin Dashboard ===\nHello, {username}!")
    users = load_users()
    print("List of all users:")
    for u, info in users.items():
        print(f"- {u} ({info['role']})")
    print("======================\n")

# User dashboard
def user_dashboard(username):
    print(f"=== User Dashboard ===\nHello, {username}!")
    print("You have standard user access.\n")

# Main menu
def main():
    while True:
        print("=== Access Control System ===")
        print("1. Signup")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":
    main()
