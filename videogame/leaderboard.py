"""
Handles leaderboard read/write using Pickle.
"""

import pickle
import os

LEADERBOARD_FILE = "leaderboard.pkl"
MAX_ENTRIES = 3


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'rb') as f:
            return pickle.load(f)
    return []


def save_leaderboard(scores):
    scores = sorted(scores, key=lambda s: s[1], reverse=True)[:MAX_ENTRIES]
    with open(LEADERBOARD_FILE, 'wb') as f:
        pickle.dump(scores, f)


def add_score(name, score):
    scores = load_leaderboard()
    scores.append((name, score))
    save_leaderboard(scores)


def is_high_score(score):
    scores = load_leaderboard()
    return len(scores) < MAX_ENTRIES or score > min(s[1] for s in scores)
