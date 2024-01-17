# login_plug.py
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
    """
    A plugin class for handling login functionality.

    Attributes:
        account (dict): Information about the logged-in user.
        user_manager (UserManager): An instance of the UserManager class for user management.

    Methods:
        __init__(self): Initializes the Plugin class.
        initialize(self, window: QMainWindow, menu: QMenuBar): Initializes the plugin and adds login-related actions to the menu.
        deinitialize(self, window, menu): Removes login-related actions from the menu.
        show_signup_dialog(self): Shows the sign-up dialog.
        show_login_dialog(self): Shows the login dialog.
        show_change_password_dialog(self): Shows the change password dialog.
        show_forget_password_dialog(self): Shows the forget password dialog.
        handle_forget_password(self): Handles the forget password action.
        authenticate_user(self, username, password): Authenticates the user with the given username and password.
        create_login_menu(self, menu): Creates the login menu and adds the login action to it.
        set_account(self, account_info): Sets the account information for the logged-in user.
        update_user_menu(self, username): Updates the user menu with the logged-in user's information.
        save_config(self): Saves the plugin configuration to a file.
        load_settings(self, settings=None): Loads the plugin configuration from a file.
        logout(self): Logs out the current user.
    """

    def __init__(self):
        """
        Initializes the LoginPlug object.
        """
        self.account = None
        self.user_manager = UserManager(users_file)  # Initialize UserManager

    def initialize(self, window: QMainWindow, menu: QMenuBar):
            """
            Initializes the login plugin.

            Args:
                window (QMainWindow): The main window of the application.
                menu (QMenuBar): The menu bar of the application.

            Returns:
                None
            """
            self.window = window
            self.create_login_menu(menu)
            self.load_settings()
            self.signup_action = QAction('Sign Up', self.window)
            self.signup_action.triggered.connect(self.show_signup_dialog)
            self.login_menu.addAction(self.signup_action)

    def deinitialize(self, window, menu):
            """
            Deinitializes the login plugin by removing the login menu action from the menu.

            Args:
                window: The main window of the application.
                menu: The menu from which the login menu action should be removed.
            """
            menu.removeAction(self.login_menu.menuAction())

    def show_signup_dialog(self):
            """
            Displays the sign-up dialog for the user to register a new account.

            This method creates an instance of the SignUpDialog class and executes it as a modal dialog.
            The register_user method from the user_manager is passed as a callback function to handle the registration process.
            The window parameter is used as the parent window for the dialog.

            Returns:
                None
            """
            dialog = SignUpDialog(self.user_manager.register_user, self.window)
            dialog.exec()

    def show_login_dialog(self):
        """
        Displays the login dialog and waits for user input.

        The method creates an instance of the LoginDialog class and executes it as a modal dialog.
        The dialog is used for user authentication and password recovery.

        Args:
            None

        Returns:
            None
        """
        dialog = LoginDialog(self.authenticate_user,
                             self.handle_forget_password, self.window)
        dialog.exec()

    def show_change_password_dialog(self):
        """
        Displays a change password dialog.

        If a user is logged in, the dialog allows the user to enter the old and new passwords.
        The change_password method of the user_manager is called with the username, old password, and new password.
        If no user is logged in, an error message is displayed.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        if self.account and 'username' in self.account:
            dialog = ChangePasswordDialog(lambda old, new: self.user_manager.change_password(
                self.account['username'], old, new), self.window)
            dialog.exec()
        else:
            QMessageBox.warning(self.window, "Error",
                                "No user is currently logged in.")

    def show_forget_password_dialog(self):
        """
        Displays a forget password dialog.

        This method creates an instance of the ForgetPasswordDialog class and
        executes it as a modal dialog. The dialog allows the user to reset their
        password by calling the `reset_password` method of the user_manager.

        Parameters:
        - self: The current instance of the LoginPlug class.

        Returns:
        - None
        """
        dialog = ForgetPasswordDialog(
            self.user_manager.reset_password, self.window)
        dialog.exec()

    def handle_forget_password(self):
        """
        Handles the forget password functionality.
        Shows the forget password dialog.
        """
        self.show_forget_password_dialog()

    def authenticate_user(self, username, password):
        """
        Authenticates the user with the provided username and password.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the authentication is successful, False otherwise.
        """
        success, message = self.user_manager.authenticate_user(
            username, password)
        QMessageBox.information(self.window, "Login", message)
        if success:
            self.set_account({'username': username})
            self.save_config()
        return success

    def create_login_menu(self, menu):
        """
        Create a login menu in the given menu.

        Parameters:
        - menu: The menu to add the login menu to.

        Returns:
        None
        """
        self.login_menu = menu.addMenu('Login')
        self.login_action = QAction('Login', self.window)
        self.login_action.triggered.connect(self.show_login_dialog)
        self.login_menu.addAction(self.login_action)

    def set_account(self, account_info):
        """
        Sets the account information for the user.

        Args:
            account_info (dict): A dictionary containing the account information.

        Returns:
            None
        """
        self.account = account_info
        self.update_user_menu(account_info['username'])

    def update_user_menu(self, username):
        """
        Update the user menu with the given username.

        Args:
            username (str): The username to be displayed in the user menu.

        Returns:
            None
        """
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
            """
            Save the plugin configuration to a JSON file.

            This method reads the existing configuration file, updates the 'login_plugin' section with the current account setting,
            and writes the updated configuration back to the file.

            Parameters:
                None

            Returns:
                None
            """
            config_key = 'login_plugin'
            config = {}
            if os.path.exists(PLUGIN_CONFIG_FILE):
                with open(PLUGIN_CONFIG_FILE, 'r') as file:
                    config = json.load(file)
            config[config_key] = {'saved_setting': self.account}
            with open(PLUGIN_CONFIG_FILE, 'w') as file:
                json.dump(config, file)

    def load_settings(self, settings=None):
            """
            Loads the settings for the login plugin.

            Args:
                settings (dict): Optional dictionary containing the settings.

            Returns:
                None
            """
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
        """
        Logs out the user by resetting the account and updating the user menu.
        """
        self.account = None
        self.update_user_menu('')
