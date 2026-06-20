import json
import os

FILE = "passwords.json"

def save_password(password):
    data = []

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []

    data.append(password)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)