import os


def filter_dirname(path: str) -> str:
    return os.path.dirname(path)


def filter_basename(path: str) -> str:
    return os.path.basename(path)
