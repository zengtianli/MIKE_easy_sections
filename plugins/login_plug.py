from PyQt6.QtWidgets import QMenuBar, QMainWindow, QMessageBox
from PyQt6.QtGui import QAction
from plugin_interface import PluginInterface
from constants import PLUGIN_CONFIG_FILE
import json
import os
import sys
from plugins.login.login_dialogs import SignUpDialog, LoginDialog, ForgetPasswordDialog, ChangePasswordDialog
from plugins.login.user_manager import UserManager  # Import UserManager
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
users_file = os.path.join(BASE_DIR, 'plugins', 'login', 'users.json')


class Plugin(PluginInterface):
    def __init__(self):
        self.account = None
        self.user_manager = UserManager(users_file)  # Initialize UserManager

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
        dialog = SignUpDialog(self.user_manager.register_user, self.window)
        dialog.exec()

    def show_login_dialog(self):
        dialog = LoginDialog(self.authenticate_user,
                             self.handle_forget_password, self.window)
        dialog.exec()

    def show_change_password_dialog(self):
        if self.account and 'username' in self.account:
            dialog = ChangePasswordDialog(lambda old, new: self.user_manager.change_password(
                self.account['username'], old, new), self.window)
            dialog.exec()
        else:
            QMessageBox.warning(self.window, "Error",
                                "No user is currently logged in.")

    def show_forget_password_dialog(self):
        dialog = ForgetPasswordDialog(
            self.user_manager.reset_password, self.window)
        dialog.exec()

    def handle_forget_password(self):
        self.show_forget_password_dialog()

    def authenticate_user(self, username, password):
        success, message = self.user_manager.authenticate_user(
            username, password)
        QMessageBox.information(self.window, "Login", message)
        if success:
            self.set_account({'username': username})
            self.save_config()
        return success

    def create_login_menu(self, menu):
        self.login_menu = menu.addMenu('Login')
        self.login_action = QAction('Login', self.window)
        self.login_action.triggered.connect(self.show_login_dialog)
        self.login_menu.addAction(self.login_action)

    def set_account(self, account_info):
        self.account = account_info
        self.update_user_menu(account_info['username'])

    def update_user_menu(self, username):
        if hasattr(self, 'user_menu'):
            self.login_menu.removeAction(self.user_menu.menuAction())
        self.user_menu = self.login_menu.addMenu(username)
        logout_action = QAction('Logout', self.window)
        logout_action.triggered.connect(self.logout)
        self.user_menu.addAction(logout_action)
        change_password_action = QAction('Change Password', self.window)
        change_password_action.triggered.connect(
            self.show_change_password_dialog)
        self.user_menu.addAction(change_password_action)

    def save_config(self):
        config_key = 'login_plugin'
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
