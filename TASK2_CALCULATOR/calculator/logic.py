import math
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "history.json")


def load_history():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_history(exp, result):
    data = load_history()
    data.append(f"{exp} = {result}")
    data = data[-20:]

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def evaluate(expression):
    try:
        allowed = {}
        allowed.update(vars(math))
        allowed.update({
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs
        })

        result = eval(expression, {"__builtins__": None}, allowed)
        result = str(result)

        save_history(expression, result)
        return result

    except:
        return "Error"