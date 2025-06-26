import json
import os
import hashlib

USER_DB = "users.json"

def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f:
            json.dump({}, f)
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password, usertype):
    users = load_users()
    if username in users:
        hashed = hash_password(password)
        return users[username]["password"] == hashed and users[username]["usertype"] == usertype
    return False

def register_user(username, password, usertype):
    users = load_users()
    if username in users:
        return False  # Already exists
    users[username] = {
        "password": hash_password(password),
        "usertype": usertype
    }
    save_users(users)
    return True
