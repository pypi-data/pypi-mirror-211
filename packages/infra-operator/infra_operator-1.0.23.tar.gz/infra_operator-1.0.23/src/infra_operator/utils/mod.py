import os


def ensure_path(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
