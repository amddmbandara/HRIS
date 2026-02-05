import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox, QDialog, QDesktopWidget,
    QMessageBox, QProgressBar
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSignal


class DesktopLoginWindow(QWidget):
    # Custom signal for successful login
    login_success = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HRM System - Desktop Login")
        self.setFixedSize(1000, 800)
        
        # Sample valid credentials (in real app, connect to database)
        self.valid_credentials = {
            "admin": "Admin@123",
            "hr.user": "Hr@2024",
            "manager": "Manager#456",
            "test.user@company.com": "Test@789"
        }
        
        # Validation states
        self.username_valid = False
        self.password_valid = False
        
        self.setup_ui()
        self.center_window()

    def setup_ui(self):
        # ================= Main Layout =================
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= LEFT PANEL =================
        left_panel = QWidget()
        left_panel.setMinimumWidth(400)
        left_panel.setMaximumWidth(450)
        left_panel.setStyleSheet("""
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e3a5f,
        stop:1 #2b6cb0
    );
    border-radius: 0px;
""")

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.setSpacing(20)

        # ===== LOGO SECTION =====
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 10, 0, 20)

        # Company Logo
        logo_label = QLabel()
        try:
            # Load the logo file
            pixmap = QPixmap('fbsl_logo.png')
            if not pixmap.isNull():
                # Scale the logo if needed
                pixmap = pixmap.scaled(600, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
            else:
                # Fallback if image is empty
                logo_label.setText("FBSL")
                logo_label.setFont(QFont("Segoe UI", 38, QFont.Bold))
                logo_label.setStyleSheet("color: white;")
                print("Warning: Logo image 'fbsl_logo.png' is empty. Using text fallback.")
        except Exception as e:
            # Fallback in case the image file is not found or can't be loaded
            logo_label.setText("FBSL")
            logo_label.setFont(QFont("Segoe UI", 38, QFont.Bold))
            logo_label.setStyleSheet("color: white;")
            print(f"Warning: Could not load logo. Error: {e}. Using text fallback.")
        
        logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(logo_label)
        left_layout.addWidget(logo_container)
        left_layout.addSpacing(5)

        brand = QLabel("Human Resource\nManagement System")
        brand.setFont(QFont("Segoe UI", 22, QFont.Bold))
        brand.setStyleSheet("color: white; line-height: 1.3;")
        brand.setAlignment(Qt.AlignCenter)
        brand.setWordWrap(True)

        welcome = QLabel("Welcome to\nFBSL ")
        welcome.setFont(QFont("Segoe UI", 26, QFont.Bold))
        welcome.setStyleSheet("color: white; margin-top: 10px;")
        welcome.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Sign in to your HR dashboard to manage\nemployees, attendance, and payroll"
        )
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #e2e8f0; line-height: 1.4;")
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignCenter)

        features = [
            "✓ Employee database management",
            "✓ Attendance & leave tracking",
            "✓ Payroll processing",
            "✓ Performance reviews",
            "✓ Reports & analytics"
        ]

        feature_box = QVBoxLayout()
        feature_box.setSpacing(5)
        for f in features:
            lbl = QLabel(f)
            lbl.setFont(QFont("Segoe UI", 10))
            lbl.setStyleSheet("color: white; padding: 2px 0;")
            lbl.setAlignment(Qt.AlignCenter)
            feature_box.addWidget(lbl)

        version = QLabel("Version 3.2.1 • Professional Edition")
        version.setFont(QFont("Segoe UI", 9))
        version.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        version.setAlignment(Qt.AlignCenter)

        left_layout.addSpacing(5)
        left_layout.addWidget(brand)
        left_layout.addSpacing(15)
        left_layout.addWidget(welcome)
        left_layout.addSpacing(5)
        left_layout.addWidget(subtitle)
        left_layout.addSpacing(20)
        left_layout.addLayout(feature_box)
        left_layout.addStretch()
        left_layout.addWidget(version)

        # ================= RIGHT PANEL =================
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: white;")

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(80, 40, 80, 40)

        title = QLabel("Account Login")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2d3748;")
        title.setAlignment(Qt.AlignCenter)

        # Username Section
        user_container = QVBoxLayout()
        user_container.setSpacing(5)
        
        user_label = QLabel("Username or Email")
        user_label.setFont(QFont("Segoe UI", 11, QFont.Medium))
        user_label.setStyleSheet("color: #4a5568;")
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter your username or email")
        self.username.setFixedHeight(42)
        self.username.setStyleSheet(self.input_style())
        self.username.textChanged.connect(self.validate_username)
        
        self.username_error = QLabel()
        self.username_error.setFont(QFont("Segoe UI", 9))
        self.username_error.setStyleSheet("color: #e53e3e; padding-left: 5px;")
        self.username_error.setVisible(False)
        
        user_container.addWidget(user_label)
        user_container.addWidget(self.username)
        user_container.addWidget(self.username_error)

        # Password Section
        pass_container = QVBoxLayout()
        pass_container.setSpacing(5)
        
        pass_label = QLabel("Password")
        pass_label.setFont(QFont("Segoe UI", 11, QFont.Medium))
        pass_label.setStyleSheet("color: #4a5568;")
        
        # Password field with show/hide toggle
        password_widget = QWidget()
        password_layout = QHBoxLayout(password_widget)
        password_layout.setContentsMargins(0, 0, 0, 0)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter your password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(42)
        self.password.setStyleSheet(self.input_style())
        self.password.textChanged.connect(self.validate_password)
        
        self.toggle_password_btn = QPushButton()
        self.toggle_password_btn.setIcon(QIcon.fromTheme("view-refresh"))
        self.toggle_password_btn.setText("👁")
        self.toggle_password_btn.setFixedSize(42, 42)
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                border: 2px solid #e2e8f0;
                border-left: none;
                border-radius: 0 8px 8px 0;
                background-color: #f8fafc;
                color: #718096;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #edf2f7;
                color: #4a5568;
            }
        """)
        self.toggle_password_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        
        password_layout.addWidget(self.password)
        password_layout.addWidget(self.toggle_password_btn)
        
        self.password_error = QLabel()
        self.password_error.setFont(QFont("Segoe UI", 9))
        self.password_error.setStyleSheet("color: #e53e3e; padding-left: 5px;")
        self.password_error.setVisible(False)
        
        # Password strength indicator
        self.password_strength = QProgressBar()
        self.password_strength.setFixedHeight(4)
        self.password_strength.setTextVisible(False)
        self.password_strength.setMaximum(100)
        self.password_strength.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #e2e8f0;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                border-radius: 2px;
            }
        """)
        self.password_strength.setVisible(False)
        
        pass_container.addWidget(pass_label)
        pass_container.addWidget(password_widget)
        pass_container.addWidget(self.password_strength)
        pass_container.addWidget(self.password_error)

        # Options
        options = QHBoxLayout()
        self.remember = QCheckBox("Remember me")
        self.remember.setFont(QFont("Segoe UI", 10))
        self.remember.setStyleSheet("""
            QCheckBox {
                color: #4a5568;
            }
        """)

        forgot = QPushButton("Forgot Password?")
        forgot.setStyleSheet(self.link_style())
        forgot.clicked.connect(self.show_forgot_dialog)

        options.addWidget(self.remember)
        options.addStretch()
        options.addWidget(forgot)

        # Login button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setFixedHeight(46)
        self.login_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.login_btn.setStyleSheet(self.login_button_style(False))
        self.login_btn.clicked.connect(self.authenticate_user)
        self.login_btn.setEnabled(False)
        
        # Enable Enter key for login
        self.login_btn.setShortcut("Return")

        # Demo credentials hint
        demo_label = QLabel("Demo credentials: admin / Admin@123")
        demo_label.setFont(QFont("Segoe UI", 9))
        demo_label.setStyleSheet("color: #a0aec0; font-style: italic;")
        demo_label.setAlignment(Qt.AlignCenter)

        footer = QLabel("© 2024 FBSL Steel Buildings • All rights reserved")
        footer.setFont(QFont("Segoe UI", 9))
        footer.setStyleSheet("color: #a0aec0;")
        footer.setAlignment(Qt.AlignCenter)

        right_layout.addStretch()
        right_layout.addWidget(title)
        right_layout.addSpacing(25)
        right_layout.addLayout(user_container)
        right_layout.addSpacing(12)
        right_layout.addLayout(pass_container)
        right_layout.addSpacing(8)
        right_layout.addLayout(options)
        right_layout.addSpacing(15)
        right_layout.addWidget(self.login_btn)
        right_layout.addSpacing(8)
        right_layout.addWidget(demo_label)
        right_layout.addStretch()
        right_layout.addWidget(footer)

        # ================= Combine Panels =================
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

    def input_style(self):
        return """
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4299e1;
                outline: none;
            }
            QLineEdit[valid="true"] {
                border-color: #38a169;
            }
            QLineEdit[valid="false"] {
                border-color: #e53e3e;
            }
        """

    def link_style(self):
        return """
            QPushButton {
                background: transparent;
                color: #4299e1;
                border: none;
                font-weight: 600;
                padding: 5px;
            }
            QPushButton:hover {
                text-decoration: underline;
                color: #3182ce;
            }
        """

    def login_button_style(self, enabled):
        if enabled:
            return """
                QPushButton {
                    background-color: #4299e1;
                    color: white;
                    border-radius: 8px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #3182ce;
                }
                QPushButton:pressed {
                    background-color: #2c5282;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #cbd5e0;
                    color: #a0aec0;
                    border-radius: 8px;
                    border: none;
                }
            """

    def validate_username(self, text):
        """Validate username/email"""
        text = text.strip()
        
        # Clear previous error
        self.username_error.clear()
        self.username_error.setVisible(False)
        self.username.setProperty("valid", "")
        self.username.style().polish(self.username)
        
        # Check if empty
        if not text:
            self.username_valid = False
            self.update_login_button()
            return
            
        # Check minimum length
        if len(text) < 3:
            self.show_username_error("Username must be at least 3 characters")
            self.username_valid = False
            self.update_login_button()
            return
            
        # Check for valid email format (if it looks like email)
        if '@' in text:
            if '.' not in text.split('@')[1] or len(text.split('@')[1].split('.')[-1]) < 2:
                self.show_username_error("Please enter a valid email address")
                self.username_valid = False
                self.update_login_button()
                return
        
        # Check for invalid characters
        invalid_chars = ['<', '>', '"', "'", ';', '(', ')', '[', ']', '{', '}', '|', '\\', '/']
        if any(char in text for char in invalid_chars):
            self.show_username_error("Contains invalid characters")
            self.username_valid = False
            self.update_login_button()
            return
            
        # Valid username
        self.username.setProperty("valid", "true")
        self.username.style().polish(self.username)
        self.username_valid = True
        self.update_login_button()

    def validate_password(self, text):
        """Validate password and show strength"""
        text = text.strip()
        
        # Clear previous error
        self.password_error.clear()
        self.password_error.setVisible(False)
        self.password.setProperty("valid", "")
        self.password.style().polish(self.password)
        
        # Check if empty
        if not text:
            self.password_strength.setVisible(False)
            self.password_valid = False
            self.update_login_button()
            return
            
        # Calculate password strength
        strength = 0
        
        # Length check
        if len(text) >= 8:
            strength += 25
        elif len(text) >= 6:
            strength += 15
            
        # Complexity checks
        if any(c.isupper() for c in text):
            strength += 20
        if any(c.islower() for c in text):
            strength += 20
        if any(c.isdigit() for c in text):
            strength += 20
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in text):
            strength += 20
            
        # Set strength bar
        self.password_strength.setValue(strength)
        self.password_strength.setVisible(True)
        
        # Color based on strength
        if strength >= 80:
            color = "#38a169"  # Green
        elif strength >= 60:
            color = "#d69e2e"  # Yellow
        elif strength >= 40:
            color = "#ed8936"  # Orange
        else:
            color = "#e53e3e"  # Red
            
        self.password_strength.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: #e2e8f0;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 2px;
            }}
        """)
        
        # Password requirements
        errors = []
        
        if len(text) < 6:
            errors.append("Minimum 6 characters")
            
        if not any(c.isupper() for c in text):
            errors.append("At least one uppercase letter")
            
        if not any(c.isdigit() for c in text):
            errors.append("At least one number")
            
        if errors:
            self.show_password_error(" • ".join(errors[:2]))
            self.password.setProperty("valid", "false")
            self.password.style().polish(self.password)
            self.password_valid = False
        else:
            self.password.setProperty("valid", "true")
            self.password.style().polish(self.password)
            self.password_valid = True
            
        self.update_login_button()

    def show_username_error(self, message):
        """Display username validation error"""
        self.username_error.setText(f"⚠ {message}")
        self.username_error.setVisible(True)
        self.username.setProperty("valid", "false")
        self.username.style().polish(self.username)

    def show_password_error(self, message):
        """Display password validation error"""
        self.password_error.setText(f"⚠ {message}")
        self.password_error.setVisible(True)
        self.password.setProperty("valid", "false")
        self.password.style().polish(self.password)

    def update_login_button(self):
        """Enable/disable login button based on validation"""
        if self.username_valid and self.password_valid:
            self.login_btn.setEnabled(True)
            self.login_btn.setStyleSheet(self.login_button_style(True))
        else:
            self.login_btn.setEnabled(False)
            self.login_btn.setStyleSheet(self.login_button_style(False))

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("🙈")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("👁")

    def authenticate_user(self):
        """Authenticate user credentials"""
        username = self.username.text().strip()
        password = self.password.text()
        
        # Check if username exists in credentials
        if username in self.valid_credentials:
            # Check if password matches
            if password == self.valid_credentials[username]:
                self.show_login_success(username)
            else:
                self.show_login_error("Invalid password. Please try again.")
        else:
            self.show_login_error("Username not found. Please check your credentials.")

    def show_login_success(self, username):
        """Show success message and proceed to main app"""
        # Disable inputs during transition
        self.username.setEnabled(False)
        self.password.setEnabled(False)
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")
        
        # Show success message
        QMessageBox.information(
            self, 
            "Login Successful",
            f"Welcome back, {username}!\n\nRedirecting to dashboard..."
        )
        
        # Emit signal for successful login (connect to main app)
        self.login_success.emit(username)
        
        # In a real app, you would close login window and open main window
        # self.close()
        # main_window.show()

    def show_login_error(self, message):
        """Show login error message"""
        QMessageBox.warning(
            self,
            "Login Failed",
            message,
            QMessageBox.Ok
        )
        
        # Clear password field and refocus
        self.password.clear()
        self.password.setFocus()
        
        # Shake animation effect
        self.shake_widget(self.password)

    def shake_widget(self, widget):
        """Simple shake animation for error feedback"""
        original_pos = widget.pos()
        for i in range(0, 5):
            if i % 2 == 0:
                widget.move(original_pos.x() + 5, original_pos.y())
            else:
                widget.move(original_pos.x() - 5, original_pos.y())
            QApplication.processEvents()
            QTimer.singleShot(50 * i, lambda: None)
        widget.move(original_pos)

    def show_forgot_dialog(self):
        """Show forgot password dialog with validation"""
        dlg = QDialog(self)
        dlg.setWindowTitle("Reset Password")
        dlg.setFixedSize(780, 520)
        dlg.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)
        
        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(25, 25, 25, 20)
        layout.setSpacing(12)
        
        title = QLabel("Reset Your Password")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #2d3748;")
        title.setAlignment(Qt.AlignCenter)
        
        desc = QLabel("Enter your registered email address to receive a password reset link.")
        desc.setFont(QFont("Segoe UI", 10))
        desc.setStyleSheet("color: #718096;")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        
        email_label = QLabel("Email Address")
        email_label.setFont(QFont("Segoe UI", 11, QFont.Medium))
        email_label.setStyleSheet("color: #4a5568;")
        
        email_input = QLineEdit()
        email_input.setPlaceholderText("name@company.com")
        email_input.setFixedHeight(40)
        email_input.setStyleSheet(self.input_style())
        
        error_label = QLabel()
        error_label.setFont(QFont("Segoe UI", 9))
        error_label.setStyleSheet("color: #e53e3e;")
        error_label.setVisible(False)
        
        def validate_email():
            email = email_input.text().strip()
            if '@' in email and '.' in email.split('@')[1] and len(email.split('@')[1].split('.')[-1]) >= 2:
                error_label.setVisible(False)
                return True
            else:
                error_label.setText("Please enter a valid email address")
                error_label.setVisible(True)
                return False
        
        button_layout = QHBoxLayout()
        
        send_btn = QPushButton("Send Reset Link")
        send_btn.setFixedHeight(40)
        send_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #48bb78;
                color: white;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #38a169;
            }
        """)
        
        def on_send():
            if validate_email():
                QMessageBox.information(
                    dlg,
                    "Reset Link Sent",
                    "If your email is registered, you will receive a password reset link shortly.",
                    QMessageBox.Ok
                )
                dlg.accept()
        
        send_btn.clicked.connect(on_send)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setFont(QFont("Segoe UI", 11))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0;
                color: #4a5568;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #cbd5e0;
            }
        """)
        cancel_btn.clicked.connect(dlg.reject)
        
        button_layout.addWidget(send_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(8)
        layout.addWidget(email_label)
        layout.addWidget(email_input)
        layout.addWidget(error_label)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        dlg.exec_()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = DesktopLoginWindow()
    
    # Connect login success signal
    def on_login_success(username):
        print(f"Login successful for user: {username}")
        # Here you would open the main application window
    
    window.login_success.connect(on_login_success)
    
    window.show()
    sys.exit(app.exec_())