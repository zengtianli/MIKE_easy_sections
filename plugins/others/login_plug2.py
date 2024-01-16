# plugins/login_plugin.py
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtGui import QAction
from plugin_interface import PluginInterface
from constants import PLUGIN_CONFIG_FILE
import json
import os

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    def setup_ui(self):
        self.setWindowTitle('Login')
        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.accept)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password)
        layout.addWidget(login_button)
    def get_credentials(self):
        return self.username.text(), self.password.text()

class Plugin(PluginInterface):
    def initialize(self, window, menu):
        self.window = window
        # self.create_login_action(menu)
        self.create_login_menu(menu)  # This line is updated

    def create_login_menu(self, menu):
        login_menu = menu.addMenu('Login')
        self.create_login_action(login_menu)

    def create_login_action(self, login_menu):
        login_action = QAction('Login', self.window)
        login_action.triggered.connect(self.show_login_dialog)
        login_menu.addAction(login_action)

    def show_login_dialog(self):
        dialog = LoginDialog(self.window)
        while dialog.exec() == QDialog.DialogCode.Accepted:
            username, password = dialog.get_credentials()
            if self.authenticate(username, password):
                break

    def authenticate(self, username, password):
        # Hardcoded credentials for demonstration purposes
        valid_username = "admin"
        valid_password = "1"
        if username == valid_username and password == valid_password:
            print("Login successful!")
            QMessageBox.information(self.window, "Login", "Login successful!")
            # Add further logic for successful login (e.g., updating UI, storing session)
            return True
        else:
            print("Invalid credentials")
            QMessageBox.critical(self.window, "Login", "Invalid credentials")
            return False

    def load_settings(self, settings):
        if 'last_logged_in_user' in settings:
            self.last_logged_in_user = settings['last_logged_in_user']
            # You can use this information to pre-fill the username in the login dialog or for other purposes

    def save_config(self, username):
        config_key = 'login_plugin'  # Plugin name without .py
        config = {}
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
        config[config_key] = {'last_logged_in_user': username}
        with open(PLUGIN_CONFIG_FILE, 'w') as file:
            json.dump(config, file)

    def set_account(self, username):
        # Logic to set the current user account
        # This could include updating the UI, enabling/disabling features, etc.
        self.current_user = username

