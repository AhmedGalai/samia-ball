import json
import os

HIGHSCORE_FILE = "highscores.json"

def load_highscores():
    """Load highscores from a JSON file."""
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as file:
            highscores = json.load(file)
    else:
        highscores = []
    highscores.sort(key=lambda x: x["score"], reverse=True)
    return highscores

def save_highscore(name, score):
    """Save a new highscore entry."""
    highscores = load_highscores()
    highscores.append({"name": name, "score": score})
    highscores.sort(key=lambda x: x["score"], reverse=True)
    with open(HIGHSCORE_FILE, "w") as file:
        json.dump(highscores, file)

def reset_highscores():
    """Clear highscores after confirmation."""
    confirmation = input("Are you sure you want to reset highscores? (y/n): ")
    if confirmation.lower() == 'y':
        with open(HIGHSCORE_FILE, "w") as file:
            json.dump([], file)
        print("Highscores reset successfully.")
