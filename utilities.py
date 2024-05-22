"""Module to work with scores"""
import os


def load_high_scores(filename="high_scores.txt"):
    """Load high scores from a file, returning a list of scores."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return [int(score.strip()) for score in file.readlines() if score.strip()]
    else:
        return []


def save_high_scores(high_scores, filename="high_scores.txt"):
    """Save high scores to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        for score in sorted(high_scores, reverse=True):
            file.write(str(score) + "\n")
