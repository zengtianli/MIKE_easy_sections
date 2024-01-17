# user_manager.py
import json
import os
import sys
import bcrypt
import base64
import random
import string
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
users_file = os.path.join(BASE_DIR, 'plugins', 'login', 'users.json')


class UserManager:
    """
    A class that manages user registration, authentication, password change, and password reset.

    Attributes:
        users_file (str): The file path to store user information.
        users (dict): A dictionary that stores the registered users and their hashed passwords.
    """


    def __init__(self, users_file):
        """
        Initialize the User Manager object.

        Args:
            users_file (str): The file path of the users file.

        Returns:
            None
        """
        self.users_file = users_file
        self.users = self.load_users()

    def register_user(self, username, password):
        """
        Register a new user with the given username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            tuple: A tuple containing a boolean value indicating the success of the registration
                   and a message describing the result.

        """
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
        return True, f"Congratulations {username}, you have successfully registered."

    @staticmethod
    def is_valid_username(username):
        return username.isalnum()

    @staticmethod
    def is_valid_password(password):
        return len(password) >= 1

    def authenticate_user(self, username, password):
        """
        Authenticates a user by checking the provided username and password against the stored user credentials.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the authentication was successful and a message string.
                - If authentication is successful, the boolean value is True and the message string is "{username}, Login successful."
                - If authentication fails, the boolean value is False and the message string is "Incorrect username or password."
        """
        user_password_hash_str = self.users.get(username)
        if user_password_hash_str:
            user_password_hash = base64.b64decode(user_password_hash_str)
            if bcrypt.checkpw(password.encode(), user_password_hash):
                return True, f"{username}, Login successful."
        return False, "Incorrect username or password."

    def change_password(self, username, old_password, new_password):
            """
            Change the password for a user.

            Args:
                username (str): The username of the user.
                old_password (str): The old password of the user.
                new_password (str): The new password to set for the user.

            Returns:
                tuple: A tuple containing a boolean indicating the success of the password change
                       and a string message describing the result.
            """
            
            if username not in self.users:
                return False, "No such user exists."
            if not self.authenticate_user(username, old_password)[0]:
                return False, "Old password is incorrect."
            if not self.is_valid_password(new_password):
                return False, "Invalid new password. It should be at least 8 characters long."
            hashed_new_password = bcrypt.hashpw(
                new_password.encode(), bcrypt.gensalt())
            hashed_new_password_str = base64.b64encode(
                hashed_new_password).decode('utf-8')
            self.users[username] = hashed_new_password_str
            self.save_users()
            return True, "Your password has been successfully changed."

    def reset_password(self, username):
            """
            Resets the password for a given username.

            Args:
                username (str): The username for which the password needs to be reset.

            Returns:
                tuple: A tuple containing a boolean value indicating the success of the password reset
                       and a string message providing information about the reset operation.
                       If the username does not exist, the boolean value will be False and the message
                       will indicate that the user does not exist. Otherwise, the boolean value will be
                       True and the message will contain the temporary password for the user.
            """
            
            if username not in self.users:
                return False, "User does not exist."
            temp_password = self.generate_temp_password()
            hashed_temp_password = bcrypt.hashpw(
                temp_password.encode(), bcrypt.gensalt())
            hashed_temp_password_str = base64.b64encode(
                hashed_temp_password).decode('utf-8')
            self.users[username] = hashed_temp_password_str
            self.save_users()
            return True, f"Temporary password for {username}: {temp_password}"

    @staticmethod
    def generate_temp_password(length=10):
        """
        Generate a temporary password of the specified length.

        Parameters:
        - length (int): The length of the generated password. Default is 10.

        Returns:
        - str: The generated temporary password.
        """
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

    def load_users(self):
            """
            Load the user data from a JSON file.

            Returns:
                dict: A dictionary containing the user data.
                      If the file doesn't exist or is empty, an empty dictionary is returned.
            """
            try:
                with open(self.users_file, 'r') as file:
                    return json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}  # Return an empty dictionary if file doesn't exist or is empty

    def save_users(self):
            """
            Save the users dictionary to a JSON file.
            """
            with open(self.users_file, 'w') as file:
                json.dump(self.users, file)
