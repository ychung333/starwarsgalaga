"""
Handles reading/writing leaderboard data using pickle.
"""

import pickle
import os
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.pkl"
MAX_ENTRIES = 3


def load_scores():
    """Load top scores from pickle file."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "rb") as file:
        return pickle.load(file)


def save_scores(scores):
    """Save top scores list to pickle file."""
    with open(LEADERBOARD_FILE, "wb") as file:
        pickle.dump(scores, file)


def is_high_score(score):
    """Check if the given score is a new high score."""
    scores = load_scores()
    return len(scores) < MAX_ENTRIES or score > min(s[1] for s in scores)


def add_score(score, name=None):
    """Add a new score (with name or datetime fallback)."""
    if name is None:
        name = datetime.now().strftime("%m-%d %H:%M")
    scores = load_scores()
    scores.append((name, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    save_scores(scores[:MAX_ENTRIES])

