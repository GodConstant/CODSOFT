def get_winner(user, computer):
    if user == computer:
        return "tie"

    if (user == "rock" and computer == "scissors") or \
       (user == "paper" and computer == "rock") or \
       (user == "scissors" and computer == "paper"):
        return "user"

    return "computer"