import os
import json
import base64
import random
import string
from hashlib import sha256

DATA_FILE = "password_store.json"

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def hash_master(master):
    return sha256(master.encode()).hexdigest()

def encrypt(data, key):
    combined = f"{data}:{key}"
    return base64.b64encode(combined.encode()).decode()

def decrypt(encoded, key):
    decoded = base64.b64decode(encoded.encode()).decode()
    data, k = decoded.split(":")
    if k == key:
        return data
    return None

def check_strength(password):
    score = 0
    if len(password) >= 12:
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    levels = ["Weak", "Moderate", "Strong", "Very Strong"]
    return levels[min(score, 3)]

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_password(master_key):
    site = input("Site name: ")
    username = input("Username: ")
    password = input("Password (leave blank to generate): ")

    if not password:
        password = generate_password()

    encrypted = encrypt(password, master_key)

    data = load_data()
    data[site] = {
        "username": username,
        "password": encrypted
    }

    save_data(data)

    print("Password saved.")
    print("Strength:", check_strength(password))

def retrieve_password(master_key):
    site = input("Enter site name: ")
    data = load_data()

    if site not in data:
        print("No entry found.")
        return

    encrypted = data[site]["password"]
    password = decrypt(encrypted, master_key)

    if password:
        print("Username:", data[site]["username"])
        print("Password:", password)
    else:
        print("Invalid master key.")

def menu():
    master = input("Enter master password: ")
    master_key = hash_master(master)

    while True:
        print("\n--- Password Manager ---")
        print("1. Generate Password")
        print("2. Save Password")
        print("3. Retrieve Password")
        print("4. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            length = int(input("Password length: "))
            print("Generated:", generate_password(length))

        elif choice == "2":
            add_password(master_key)

        elif choice == "3":
            retrieve_password(master_key)

        elif choice == "4":
            print("Goodbye")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()