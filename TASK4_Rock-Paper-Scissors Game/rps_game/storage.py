import json
import os

FILE = "stats.json"

def load_stats():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return {"user": 0, "computer": 0}
    return {"user": 0, "computer": 0}

def save_stats(stats):
    with open(FILE, "w") as f:
        json.dump(stats, f, indent=4)