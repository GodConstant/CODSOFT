import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from game_logic import get_winner
from ai import get_computer_choice
from storage import load_stats, save_stats


class RPSApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rock Paper Scissors")
        self.setMinimumSize(400, 300)
        self.resize(600, 400)

        self.stats = load_stats()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # Title
        title = QLabel("🎮 Rock Paper Scissors")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Result
        self.result_label = QLabel("Make your move")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Score
        self.score_label = QLabel(self.get_score_text())
        self.score_label.setAlignment(Qt.AlignCenter)

        # Buttons
        btn_layout = QHBoxLayout()

        for choice in ["rock", "paper", "scissors"]:
            btn = QPushButton(choice.capitalize())
            btn.clicked.connect(lambda _, c=choice: self.play(c))
            btn_layout.addWidget(btn)

        # Reset button
        reset_btn = QPushButton("Reset Score")
        reset_btn.clicked.connect(self.reset_score)

        # Layout
        main_layout.addWidget(title)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.score_label)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(reset_btn)

        self.setLayout(main_layout)

    def get_score_text(self):
        return f"You: {self.stats['user']} | Computer: {self.stats['computer']}"

    def play(self, user_choice):
        computer_choice = get_computer_choice()
        winner = get_winner(user_choice, computer_choice)

        if winner == "user":
            self.stats["user"] += 1
            result = "You Win!"
        elif winner == "computer":
            self.stats["computer"] += 1
            result = "Computer Wins!"
        else:
            result = "It's a Tie!"

        save_stats(self.stats)

        self.result_label.setText(
            f"You: {user_choice} | Computer: {computer_choice}\n{result}"
        )
        self.score_label.setText(self.get_score_text())

    def reset_score(self):
        self.stats = {"user": 0, "computer": 0}
        save_stats(self.stats)
        self.score_label.setText(self.get_score_text())
        self.result_label.setText("Score Reset")