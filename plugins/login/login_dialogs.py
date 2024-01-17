from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMenuBar, QMainWindow, QMessageBox
from PyQt6.QtGui import QIcon, QFont
BUTTON_STYLE = "QPushButton { background-color: #007bff; color: white; border-radius: 4px; }"
EDIT_STYLE = "QLineEdit { border: 1px solid #ced4da; border-radius: 4px; padding: 6px; }"
LABEL_STYLE = "QLabel { color: #495057; }"


class SignUpDialog(QDialog):
    """
    A dialog window for user sign up.

    Args:
        register_callback (function): A callback function to handle the registration process.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, register_callback, parent=None):
        """
        Initialize the LoginDialog instance.

        Args:
            register_callback (function): The callback function to be called when the user signs up.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.register_callback = register_callback
        self.setWindowTitle("Sign Up")
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        # Username
        label_username = QLabel("Username:")
        label_username.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_username)
        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText("Enter your username")
        self.username_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.username_edit)
        # Password
        label_password = QLabel("Password:")
        label_password.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_password)
        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText("Enter your password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.password_edit)
        # Confirm Password
        label_confirm = QLabel("Confirm Password:")
        label_confirm.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_confirm)
        self.password_confirm_edit = QLineEdit(self)
        self.password_confirm_edit.setPlaceholderText("Confirm your password")
        self.password_confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_confirm_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.password_confirm_edit)
        # Sign Up Button
        signup_button = QPushButton("Sign Up", self)
        signup_button.setStyleSheet(BUTTON_STYLE)
        signup_button.clicked.connect(self.handle_signup)
        layout.addWidget(signup_button)

    def handle_signup(self):
        """
        Handles the sign-up process.

        Retrieves the username, password, and password confirmation from the input fields.
        Checks if the passwords match. If not, displays an error message.
        Calls the register_callback method to register the user.
        If registration is successful, displays a success message and closes the dialog.
        If registration fails, displays an error message.

        Returns:
            None
        """
        username = self.username_edit.text()
        password = self.password_edit.text()
        password_confirm = self.password_confirm_edit.text()
        if password != password_confirm:
            QMessageBox.warning(self, "Sign Up Failed",
                                "Passwords do not match.")
            return
        success, message = self.register_callback(username, password)
        if success:
            QMessageBox.information(self, "Registration Successful", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Sign Up Failed", message)


class LoginDialog(QDialog):
    """
    A dialog for user login.

    Args:
        authenticate_callback (function): A callback function for authenticating the user.
        forget_password_callback (function): A callback function for handling forget password action.
        parent (QWidget): The parent widget of the dialog.

    Attributes:
        authenticate_callback (function): A callback function for authenticating the user.
        forget_password_callback (function): A callback function for handling forget password action.
        username_edit (QLineEdit): The QLineEdit widget for entering the username.
        password_edit (QLineEdit): The QLineEdit widget for entering the password.

    """

    def __init__(self, authenticate_callback, forget_password_callback, parent=None):
        """
        Initialize the LoginDialog.

        Args:
            authenticate_callback (function): The callback function to be called when the user attempts to authenticate.
            forget_password_callback (function): The callback function to be called when the user forgets their password.
            parent (QWidget): The parent widget of the LoginDialog.

        Returns:
            None
        """

        super().__init__(parent)
        self.authenticate_callback = authenticate_callback
        self.forget_password_callback = forget_password_callback
        self.setWindowTitle("Login")
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface of the login dialog.
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        # Username
        label_username = QLabel("Username:")
        label_username.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_username)
        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText("Enter your username")
        self.username_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.username_edit)
        # Password
        label_password = QLabel("Password:")
        label_password.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_password)
        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText("Enter your password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.password_edit)
        # Login Button
        login_button = QPushButton("Login", self)
        login_button.setStyleSheet(BUTTON_STYLE)
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        # Forget Password Button
        forget_password_button = QPushButton("Forget Password", self)
        forget_password_button.setStyleSheet(BUTTON_STYLE)
        forget_password_button.clicked.connect(self.handle_forget_password)
        layout.addWidget(forget_password_button)

    def handle_login(self):
        """
        Handle the login button click event.
        """
        username = self.username_edit.text()
        password = self.password_edit.text()
        if self.authenticate_callback(username, password):
            self.accept()  # Close the dialog only on successful login
        else:
            pass

    def handle_forget_password(self):
        """
        Handle the forget password button click event.
        """
        self.forget_password_callback()


class ForgetPasswordDialog(QDialog):
    """
    Dialog for resetting password.

    Args:
        reset_password_callback (function): Callback function for resetting password.
        parent (QWidget, optional): Parent widget. Defaults to None.
    """

    def __init__(self, reset_password_callback, parent=None):
        super().__init__(parent)
        self.reset_password_callback = reset_password_callback
        self.setWindowTitle("Forget Password")
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface of the dialog.
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        # Username
        label_username = QLabel("Username:")
        label_username.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_username)
        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText("Enter your username")
        self.username_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.username_edit)
        # Reset Password Button
        reset_password_button = QPushButton("Reset Password", self)
        reset_password_button.setStyleSheet(BUTTON_STYLE)
        reset_password_button.clicked.connect(self.handle_reset_password)
        layout.addWidget(reset_password_button)

    def handle_reset_password(self):
        """
        Handle the reset password button click event.
        """
        username = self.username_edit.text()
        success, message = self.reset_password_callback(username)
        if success:
            QMessageBox.information(self, "Reset Password", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Reset Password Failed", message)


class ChangePasswordDialog(QDialog):
    """
    Dialog window for changing the password.

    Args:
        change_password_callback (function): A callback function that is called when the password is changed.
        parent (QWidget, optional): The parent widget of the dialog.

    Attributes:
        old_password_edit (QLineEdit): The QLineEdit widget for entering the old password.
        new_password_edit (QLineEdit): The QLineEdit widget for entering the new password.
        confirm_new_password_edit (QLineEdit): The QLineEdit widget for confirming the new password.

    Signals:
        None

    """

    def __init__(self, change_password_callback, parent=None):
        """
        Initialize the LoginDialog instance.

        Args:
            change_password_callback (function): The callback function to be called when the password is changed.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.change_password_callback = change_password_callback
        self.setWindowTitle("Change Password")
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for the login dialog.

        This method creates and configures the various UI elements such as labels, text fields, and buttons
        for the login dialog. It also connects the "Change Password" button to the `handle_change_password` method.

        Parameters:
            None

        Returns:
            None
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        # Old Password
        label_old_password = QLabel("Old Password:")
        label_old_password.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_old_password)
        self.old_password_edit = QLineEdit(self)
        self.old_password_edit.setPlaceholderText("Enter your old password")
        self.old_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_password_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.old_password_edit)
        # New Password
        label_new_password = QLabel("New Password:")
        label_new_password.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_new_password)
        self.new_password_edit = QLineEdit(self)
        self.new_password_edit.setPlaceholderText("Enter your new password")
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.new_password_edit)
        # Confirm New Password
        label_confirm_password = QLabel("Confirm New Password:")
        label_confirm_password.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label_confirm_password)
        self.confirm_new_password_edit = QLineEdit(self)
        self.confirm_new_password_edit.setPlaceholderText(
            "Confirm your new password")
        self.confirm_new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_new_password_edit.setStyleSheet(EDIT_STYLE)
        layout.addWidget(self.confirm_new_password_edit)
        # Change Password Button
        change_password_button = QPushButton("Change Password", self)
        change_password_button.setStyleSheet(BUTTON_STYLE)
        change_password_button.clicked.connect(self.handle_change_password)
        layout.addWidget(change_password_button)

    def handle_change_password(self):
        """
        Handles the change password functionality.

        Retrieves the old password, new password, and confirm new password from the input fields.
        Checks if the new passwords match. If not, displays a warning message.
        Calls the change_password_callback function with the old and new passwords.
        If the password change is successful, displays an information message and accepts the dialog.
        Otherwise, displays a warning message with the error message.

        Returns:
            None
        """
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        confirm_new_password = self.confirm_new_password_edit.text()
        if new_password != confirm_new_password:
            QMessageBox.warning(self, "Change Password Failed",
                                "New passwords do not match.")
            return
        success, message = self.change_password_callback(
            old_password, new_password)
        if success:
            QMessageBox.information(self, "Change Password", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Change Password Failed", message)
