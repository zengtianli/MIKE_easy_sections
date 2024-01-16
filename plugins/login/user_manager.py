# user_manager.py
import json
import os,sys
import bcrypt, base64
import random, string
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
users_file = os.path.join(BASE_DIR, 'plugins', 'login', 'users.json')
class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.users = self.load_users()
    def register_user(self, username, password):
        if not self.is_valid_username(username):
            return False, "Invalid username. It should be alphanumeric."
        if not self.is_valid_password(password):
            return False, "Invalid password. It should be at least 8 characters long."
        if username in self.users:
            return False, "User already exists."
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
        self.users[username] = hashed_password_str
        self.save_users()
        return True, f"Congratulation {username}, you have successfully registered."
    @staticmethod
    def is_valid_username(username):
        return username.isalnum()
    @staticmethod
    def is_valid_password(password):
        return len(password) >= 1
    def authenticate_user(self, username, password):
        user_password_hash_str = self.users.get(username)
        if user_password_hash_str:
            user_password_hash = base64.b64decode(user_password_hash_str)
            if bcrypt.checkpw(password.encode(), user_password_hash):
                return True, f"{username}, Login successful."
        return False, "Incorrect username or password."
    def change_password(self, username, old_password, new_password):
        if username not in self.users:
            return False, "No such user exists."
        if not self.authenticate_user(username, old_password)[0]:
            return False, "Old password is incorrect."
        if not self.is_valid_password(new_password):
            return False, "Invalid new password. It should be at least 8 characters long."
        hashed_new_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        hashed_new_password_str = base64.b64encode(hashed_new_password).decode('utf-8')
        self.users[username] = hashed_new_password_str
        self.save_users()
        return True, "Your password has been successfully changed."
    def reset_password(self, username):
        if username not in self.users:
            return False, "User does not exist."
        temp_password = self.generate_temp_password()
        hashed_temp_password = bcrypt.hashpw(temp_password.encode(), bcrypt.gensalt())
        hashed_temp_password_str = base64.b64encode(hashed_temp_password).decode('utf-8')
        self.users[username] = hashed_temp_password_str
        self.save_users()
        return True, f"Temporary password for {username}: {temp_password}"
    @staticmethod
    def generate_temp_password(length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))
    def load_users(self):
        try:
            with open(self.users_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Return an empty dictionary if file doesn't exist or is empty
    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file)
