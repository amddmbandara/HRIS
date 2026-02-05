import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HRM System - Registration")
        self.setFixedSize(900, 500)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ================= LEFT LOGO PANEL =================
        left_panel = QFrame()
        left_panel.setFixedWidth(300)
        left_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e3a5f,
                    stop:1 #2b6cb0
                );
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 50, 20, 20)
        left_layout.setSpacing(10)

        # Logo
        logo_label = QLabel()
        try:
            pixmap = QPixmap('fbsl_logo.png')
            if not pixmap.isNull():
                pixmap = pixmap.scaled(180, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
            else:
                raise Exception("Pixmap is null")
        except:
            logo_label.setText("FBSL")
            logo_label.setFont(QFont("Segoe UI", 38, QFont.Bold))
            logo_label.setStyleSheet("color: white;")
        logo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(logo_label, alignment=Qt.AlignTop)

        # Welcome Text
        welcome_label = QLabel("Welcome to FBSL HRM System!\nPlease register below.")
        welcome_label.setWordWrap(True)
        welcome_label.setFont(QFont("Segoe UI", 11))
        welcome_label.setStyleSheet("color: white;")
        welcome_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        left_layout.addSpacing(30)
        left_layout.addWidget(welcome_label)
        left_layout.addStretch()

        # ================= RIGHT FORM PANEL =================
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: white; 
                border-radius: 12px;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(10)

        # Header
        header = QLabel("Register New Employee")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("color: #1e3a5f;")
        right_layout.addWidget(header, alignment=Qt.AlignTop)
        right_layout.addSpacing(10)

        # ----- Form Fields -----
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.name_input.setFixedHeight(28)
        self.name_error = QLabel()
        self.name_error.setStyleSheet("color: red; font-size: 10px;")
        self.name_error.setFixedHeight(12)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setFixedHeight(28)
        self.email_error = QLabel()
        self.email_error.setStyleSheet("color: red; font-size: 10px;")
        self.email_error.setFixedHeight(12)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(28)
        self.password_error = QLabel()
        self.password_error.setStyleSheet("color: red; font-size: 10px;")
        self.password_error.setFixedHeight(12)

        self.position_input = QComboBox()
        self.position_input.addItems(["HR", "Project Manager", "Director"])
        self.position_input.setFixedHeight(28)

        # Add fields
        right_layout.addWidget(self.name_input)
        right_layout.addWidget(self.name_error)
        right_layout.addWidget(self.email_input)
        right_layout.addWidget(self.email_error)
        right_layout.addWidget(self.password_input)
        right_layout.addWidget(self.password_error)
        right_layout.addWidget(self.position_input)

        # ----- Buttons -----
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setFixedHeight(30)
        self.submit_btn.setStyleSheet("background-color:#4299e1; color:white; border-radius:5px;")
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedHeight(30)
        self.cancel_btn.setStyleSheet("background-color:#e2e8f0; color:#2d3748; border-radius:5px;")
        btn_layout.addWidget(self.submit_btn)
        btn_layout.addWidget(self.cancel_btn)
        right_layout.addSpacing(10)
        right_layout.addLayout(btn_layout)
        right_layout.addStretch()

        # ================= Assemble Main Layout =================
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 2)  # Right panel takes more space

        # ================= Signals =================
        self.name_input.textChanged.connect(self.validate_name)
        self.email_input.textChanged.connect(self.validate_email)
        self.password_input.textChanged.connect(self.validate_password)

        # Optional: connect buttons
        self.submit_btn.clicked.connect(self.submit_form)
        self.cancel_btn.clicked.connect(self.close)

    # -------- Validation Functions --------
    def validate_name(self):
        text = self.name_input.text()
        self.name_error.setText("" if len(text.strip()) >= 3 else "Name must be at least 3 characters")

    def validate_email(self):
        text = self.email_input.text()
        self.email_error.setText("" if re.match(r"[^@]+@[^@]+\.[^@]+", text) else "Invalid email format")

    def validate_password(self):
        text = self.password_input.text()
        self.password_error.setText("" if len(text) >= 6 else "Password must be at least 6 characters")

    # -------- Button Actions --------
    def submit_form(self):
        self.validate_name()
        self.validate_email()
        self.validate_password()
        if not self.name_error.text() and not self.email_error.text() and not self.password_error.text():
            print("Form Submitted:")
            print("Name:", self.name_input.text())
            print("Email:", self.email_input.text())
            print("Position:", self.position_input.currentText())
        else:
            print("Fix the errors before submitting.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())
