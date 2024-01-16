from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMenuBar, QMainWindow, QMessageBox
from PyQt6.QtGui import QIcon, QFont
BUTTON_STYLE = "QPushButton { background-color: #007bff; color: white; border-radius: 4px; }"
EDIT_STYLE = "QLineEdit { border: 1px solid #ced4da; border-radius: 4px; padding: 6px; }"
LABEL_STYLE = "QLabel { color: #495057; }"


class SignUpDialog(QDialog):
    def __init__(self, register_callback, parent=None):
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
    def __init__(self, authenticate_callback, forget_password_callback, parent=None):
        super().__init__(parent)
        self.authenticate_callback = authenticate_callback
        self.forget_password_callback = forget_password_callback
        self.setWindowTitle("Login")
        self.setup_ui()

    def setup_ui(self):
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
        username = self.username_edit.text()
        password = self.password_edit.text()
        if self.authenticate_callback(username, password):
            self.accept()  # Close the dialog only on successful login
        else:
            pass

    def handle_forget_password(self):
        self.forget_password_callback()


class ForgetPasswordDialog(QDialog):
    def __init__(self, reset_password_callback, parent=None):
        super().__init__(parent)
        self.reset_password_callback = reset_password_callback
        self.setWindowTitle("Forget Password")
        self.setup_ui()

    def setup_ui(self):
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
        username = self.username_edit.text()
        success, message = self.reset_password_callback(username)
        if success:
            QMessageBox.information(self, "Reset Password", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Reset Password Failed", message)


class ChangePasswordDialog(QDialog):
    def __init__(self, change_password_callback, parent=None):
        super().__init__(parent)
        self.change_password_callback = change_password_callback
        self.setWindowTitle("Change Password")
        self.setup_ui()

    def setup_ui(self):
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
