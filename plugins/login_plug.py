from PyQt6.QtWidgets import QMenuBar, QMainWindow,QMessageBox
from PyQt6.QtGui import QAction
from plugin_interface import PluginInterface
from constants import PLUGIN_CONFIG_FILE
import json
import os,sys
import bcrypt,base64
import string  # Import the string module
import random  # Import the random module
from plugins.login.login_dialogs import SignUpDialog, LoginDialog, ForgetPasswordDialog, ChangePasswordDialog
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
users_file = os.path.join(BASE_DIR,'plugins','login', 'users.json')
class Plugin(PluginInterface):
    def __init__(self):
        self.account = None  # Holds account details
        self.users_file = users_file # File to store user data
        self.users = self.load_users()  # Load users from the file
    # def register_user(self, username, password):
    #     if not self.is_valid_username(username):
    #         QMessageBox.warning(self.window, "Registration Failed", "Invalid username. It should be alphanumeric.")
    #         return False
    #     if not self.is_valid_password(password):
    #         QMessageBox.warning(self.window, "Registration Failed", "Invalid password. It should be at least 8 characters long.")
    #         return False
    #     if username in self.users:
    #         QMessageBox.warning(self.window, "Registration Failed", "User already exists.")
    #         return False  # User already exists
    #     hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    #     hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
    #     self.users[username] = hashed_password_str
    #     message = f"Congratulation <b>{username}</b>, you have successfully registered."
    #     QMessageBox.information(self.window, "Registration Successful", message)
    #     self.save_users()
    #     return True
    # @staticmethod
    # def is_valid_username(username):
    #     return username.isalnum()
    # @staticmethod
    # def is_valid_password(password):
    #     return len(password) >= 1
    # def authenticate_user(self, username, password):
    #     user_password_hash_str = self.users.get(username)
    #     if user_password_hash_str:
    #         user_password_hash = base64.b64decode(user_password_hash_str)
    #         if bcrypt.checkpw(password.encode(), user_password_hash):
    #             self.set_account({'username': username})
    #             self.save_config()
    #             return True
    #     return False
    def initialize(self, window: QMainWindow, menu: QMenuBar):
        self.window = window
        self.create_login_menu(menu)
        self.load_settings()
        self.signup_action = QAction('Sign Up', self.window)
        self.signup_action.triggered.connect(self.show_signup_dialog)
        self.login_menu.addAction(self.signup_action)
    def deinitialize(self, window, menu):
        menu.removeAction(self.login_menu.menuAction())
    def show_signup_dialog(self):
        dialog = SignUpDialog(self.register_user, self.window) 
        dialog.exec()
    def show_forget_password_dialog(self):
        dialog = ForgetPasswordDialog(self.reset_password, self.window) 
        dialog.exec()
    def show_login_dialog(self):
        dialog = LoginDialog(self.authenticate_user, self.handle_forget_password, self.window) 
        dialog.exec()
    def show_change_password_dialog(self):
        dialog = ChangePasswordDialog(self.change_password, self.window)
        dialog.exec()
    # def change_password(self, old_password, new_password):
    #     if not self.account or 'username' not in self.account:
    #         QMessageBox.warning(self.window, "Change Password Failed", "No user is currently logged in.")
    #         return
    #     if not self.authenticate_user(self.account['username'], old_password):
    #         QMessageBox.warning(self.window, "Change Password Failed", "Old password is incorrect.")
    #         return
    #     if not self.is_valid_password(new_password):
    #         QMessageBox.warning(self.window, "Change Password Failed", "Invalid new password. It should be at least 8 characters long.")
    #         return
    #     hashed_new_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    #     hashed_new_password_str = base64.b64encode(hashed_new_password).decode('utf-8')
    #     self.users[self.account['username']] = hashed_new_password_str
    #     self.save_users()
    #     QMessageBox.information(self.window, "Change Password", "Your password has been successfully changed.")
    def handle_forget_password(self):
        forget_password_dialog = ForgetPasswordDialog(self.reset_password, self.window)
        forget_password_dialog.exec()
    # def reset_password(self, username):
    #     if username not in self.users:
    #         QMessageBox.warning(self.window, "Reset Password Failed", "User does not exist.")
    #         return False
    #     temp_password = self.generate_temp_password()
    #     hashed_temp_password = bcrypt.hashpw(temp_password.encode(), bcrypt.gensalt())
    #     hashed_temp_password_str = base64.b64encode(hashed_temp_password).decode('utf-8')
    #     self.users[username] = hashed_temp_password_str
    #     self.save_users()
    #     print(f"Temporary password for {username}: {temp_password}")  # For demonstration only
    #     QMessageBox.information(self.window, "Reset Password", "Your password has been reset. Please check your email for the temporary password.")
    #     return True
    # @staticmethod
    # def generate_temp_password(length=10):
    #     characters = string.ascii_letters + string.digits
    #     return ''.join(random.choice(characters) for i in range(length))
    def update_user_menu(self, username):
        if hasattr(self, 'user_menu'):
            self.login_menu.removeAction(self.user_menu.menuAction())
        self.user_menu = self.login_menu.addMenu(username)
        logout_action = QAction('Logout', self.window)
        logout_action.triggered.connect(self.logout)
        self.user_menu.addAction(logout_action)
        change_password_action = QAction('Change Password', self.window)
        change_password_action.triggered.connect(self.show_change_password_dialog)
        self.user_menu.addAction(change_password_action)
    def create_login_menu(self, menu):
        self.login_menu = menu.addMenu('Login')
        self.login_action = QAction('Login', self.window)
        self.login_action.triggered.connect(self.show_login_dialog)
        self.login_menu.addAction(self.login_action)
    def set_account(self, account_info):
        self.account = account_info
        self.update_user_menu(account_info['username'])  # Update the menu with the user's name
        self.save_config()
    def save_config(self):
        config_key = 'login_plugin'  # Unique key for this plugin's settings
        config = {}
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
        config[config_key] = {'saved_setting': self.account}
        with open(PLUGIN_CONFIG_FILE, 'w') as file:
            json.dump(config, file)
    def load_settings(self, settings=None):
        if settings is not None:
            self.account = settings.get('saved_setting', {})
            if self.account and 'username' in self.account:
                self.update_user_menu(self.account['username'])
        else:
            if os.path.exists(PLUGIN_CONFIG_FILE):
                with open(PLUGIN_CONFIG_FILE, 'r') as file:
                    config = json.load(file)
                    plugin_config = config.get('login_plugin', {})
                    self.account = plugin_config.get('saved_setting')
                    if self.account and 'username' in self.account:
                        self.update_user_menu(self.account['username'])
    def logout(self):
        self.account = None
        self.update_user_menu('')
    # def load_users(self):
    #     try:
    #         with open(self.users_file, 'r') as file:
    #             return json.load(file)
    #     except (FileNotFoundError, json.JSONDecodeError):
    #         return {}  # Return an empty dictionary if file doesn't exist or is empty
    # def save_users(self):
    #     with open(self.users_file, 'w') as file:
    #         json.dump(self.users, file)
