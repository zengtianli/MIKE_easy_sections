# plugins/login_plugin.py
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMenuBar, QMainWindow,QMessageBox
from PyQt6.QtGui import QAction
from plugin_interface import PluginInterface
from constants import PLUGIN_CONFIG_FILE
import json
import os
class SignUpDialog(QDialog):
    def __init__(self, register_callback, parent=None):
        super().__init__(parent)
        self.register_callback = register_callback
        self.setWindowTitle("Sign Up")
        layout = QVBoxLayout(self)
        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText("Username")
        layout.addWidget(self.username_edit)
        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)
        self.password_confirm_edit = QLineEdit(self)
        self.password_confirm_edit.setPlaceholderText("Confirm Password")
        self.password_confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_confirm_edit)
        signup_button = QPushButton("Sign Up", self)
        signup_button.clicked.connect(self.handle_signup)
        layout.addWidget(signup_button)
    def handle_signup(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        password_confirm = self.password_confirm_edit.text()
        if password != password_confirm:
            QMessageBox.warning(self, "Sign Up Failed", "Passwords do not match.")
            return
        if self.register_callback(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Sign Up Failed", "Could not create account.")
class LoginDialog(QDialog):
    def __init__(self, authenticate_callback, parent=None):
        super().__init__(parent)
        self.authenticate_callback = authenticate_callback
        self.setWindowTitle("Login")
        layout = QVBoxLayout(self)
        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText("Username")
        layout.addWidget(self.username_edit)
        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_edit)
        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        if self.authenticate_callback(username, password):
            self.accept()  # Close the dialog only on successful login
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password. Please try again.")
class Plugin(PluginInterface):
    def __init__(self):
        self.account = None  # Holds account details
        self.users_file = "users.json"  # File to store user data
        self.users = self.load_users()  # Load users from the file
    def register_user(self, username, password):
        self.users[username] = password
        return True
    def initialize(self, window: QMainWindow, menu: QMenuBar):
        self.window = window
        self.create_login_menu(menu)
        self.load_settings()
        self.signup_action = QAction('Sign Up', self.window)
        self.signup_action.triggered.connect(self.show_signup_dialog)
        self.login_menu.addAction(self.signup_action)
    def show_signup_dialog(self):
        dialog = SignUpDialog(self.register_user, self.window)
        dialog.exec()
    def create_login_menu(self, menu):
        self.login_menu = menu.addMenu('Login')
        self.login_action = QAction('Login', self.window)
        self.login_action.triggered.connect(self.show_login_dialog)
        self.login_menu.addAction(self.login_action)
    def show_login_dialog(self):
        dialog = LoginDialog(self.authenticate_user, self.window)
        dialog.exec()
    def authenticate_user(self, username, password):
        if username == "admin" and password == "a":
            self.set_account({'username': username})
            print("Account set, now saving...")  # Debugging print
            self.save_config()
            return True
        else:
            return False
    def deinitialize(self, window, menu):
        menu.removeAction(self.login_menu.menuAction())
    def set_account(self, account_info):
        self.account = account_info
        self.update_user_menu(account_info['username'])  # Update the menu with the user's name
        self.save_config()
    def set_account(self, account_info):
        self.account = account_info
        self.update_user_menu(account_info['username'])  # Update the menu with the user's name
        self.save_config()
    def update_user_menu(self, username):
        # Remove the old user menu if it exists
        if hasattr(self, 'user_menu'):
            self.login_menu.removeAction(self.user_menu.menuAction())
        # Create a new menu item with the user's name
        self.user_menu = self.login_menu.addMenu(username)
        # Add any actions you want to this menu
        # For example, a logout action
        logout_action = QAction('Logout', self.window)
        logout_action.triggered.connect(self.logout)
        self.user_menu.addAction(logout_action)
    def save_config(self):
        config_key = 'login_plugin'  # Unique key for this plugin's settings
        config = {}
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
        config[config_key] = {'saved_setting': self.account}
        with open(PLUGIN_CONFIG_FILE, 'w') as file:
            json.dump(config, file)

    # def load_settings(self):
    #     if os.path.exists(PLUGIN_CONFIG_FILE):
    #         with open(PLUGIN_CONFIG_FILE, 'r') as file:
    #             config = json.load(file)
    #             plugin_config = config.get('login_plugin', {})
    #             self.account = plugin_config.get('saved_setting')
    #             if self.account and 'username' in self.account:
    #                 # Update the user menu with the saved username
    #                 self.update_user_menu(self.account['username'])

    def load_settings(self, settings=None):
        if settings is not None:
            self.account = settings.get('saved_setting', {})
            if self.account and 'username' in self.account:
                self.update_user_menu(self.account['username'])
        else:
            # Existing logic for loading settings directly from the config file
            if os.path.exists(PLUGIN_CONFIG_FILE):
                with open(PLUGIN_CONFIG_FILE, 'r') as file:
                    config = json.load(file)
                    plugin_config = config.get('login_plugin', {})
                    self.account = plugin_config.get('saved_setting')
                    if self.account and 'username' in self.account:
                        self.update_user_menu(self.account['username'])
    def logout(self):
        # Reset the account information and update the menu
        self.account = None
        self.update_user_menu('')
    def load_users(self):
        try:
            with open(self.users_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Return an empty dictionary if file doesn't exist or is empty
    def register_user(self, username, password):
        if username in self.users:
            return False  # User already exists
        self.users[username] = password  # Add the new user
        self.save_users()  # Save updated users list
        return True
    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file)
