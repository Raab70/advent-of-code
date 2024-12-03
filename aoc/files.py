from pathlib import Path


def readlines(task: int):
    path = Path(f"./data/input{task}.txt")
    if not path.is_file():
        raise FileNotFoundError(f"File {path.absolute()} not found")
    with open(path) as f:
        return f.read().splitlines()
