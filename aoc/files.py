from pathlib import Path
from rich import print


def get_path(day: int):
    return Path(f"./data/input{day}.txt")


def readlines(day: int):
    path = get_path(day)
    if not path.is_file():
        raise FileNotFoundError(f"File {path.absolute()} not found")
    with open(path) as f:
        return f.read().splitlines()


def write_input(day: int, data: str):
    path = get_path(day)
    with open(path, "w") as f:
        f.write(data)
    print(f"Input for day {day} written to {path.absolute()}")
