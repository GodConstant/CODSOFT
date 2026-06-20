import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QCheckBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from generator import generate_password
from password_generator.strength import check_strength
from password_generator.utils import save_password


class PasswordApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Generator")
        self.setMinimumSize(400, 300)
        self.resize(1200, 1000)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        # Title
        title = QLabel(" Password Generator")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Input
        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Enter password length")

        # Options
        self.digits_checkbox = QCheckBox("Include Digits")
        self.digits_checkbox.setChecked(True)

        self.symbols_checkbox = QCheckBox("Include Symbols")
        self.symbols_checkbox.setChecked(True)

        # Buttons
        btn_layout = QHBoxLayout()
        generate_btn = QPushButton("Generate")
        save_btn = QPushButton("Save")

        generate_btn.clicked.connect(self.handle_generate)
        save_btn.clicked.connect(self.handle_save)

        btn_layout.addWidget(generate_btn)
        btn_layout.addWidget(save_btn)

        # Result display
        self.result_label = QLabel("")
        self.result_label.setStyleSheet(
            "border: 1px solid gray; padding: 8px; background: #f5f5f5;"
        )
        self.result_label.setAlignment(Qt.AlignCenter)

        # Strength
        self.strength_label = QLabel("Strength: -")
        self.strength_label.setAlignment(Qt.AlignCenter)

        # Copy button
        copy_btn = QPushButton("Copy Password")
        copy_btn.clicked.connect(self.copy_password)

        # Add everything
        main_layout.addWidget(title)
        main_layout.addWidget(self.length_input)
        main_layout.addWidget(self.digits_checkbox)
        main_layout.addWidget(self.symbols_checkbox)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.strength_label)
        main_layout.addWidget(copy_btn)

        self.setLayout(main_layout)

    def handle_generate(self):
        try:
            length = int(self.length_input.text())
            if length <= 0:
                raise ValueError
        except:
            self.result_label.setText("Invalid length")
            self.strength_label.setText("Strength: -")
            return

        password = generate_password(
            length,
            self.digits_checkbox.isChecked(),
            self.symbols_checkbox.isChecked()
        )

        strength = check_strength(password)

        self.result_label.setText(password)
        self.strength_label.setText(f"Strength: {strength}")

    def handle_save(self):
        password = self.result_label.text()

        if not password or "Invalid" in password:
            self.strength_label.setText("Nothing to save")
            return

        save_password(password)
        self.strength_label.setText("Saved successfully ✔")

    def copy_password(self):
        password = self.result_label.text()
        if password:
            QApplication.clipboard().setText(password)
            self.strength_label.setText("Copied to clipboard ✔")


app = QApplication(sys.argv)
window = PasswordApp()
window.show()
sys.exit(app.exec_())