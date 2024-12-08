from pathlib import Path

from rich import print


def get_py_template_path():
    return Path("./_template.py")


def get_py_path(day: int):
    return Path(f"./day{day}.py")


def create_day_from_template(day: int):
    template_path = get_py_template_path()
    if not template_path.is_file():
        raise FileNotFoundError(f"Template file {template_path.absolute()} not found")
    pypath = get_py_path(day)
    with open(template_path) as f:
        template = f.read()
    with open(pypath, "w") as f:
        f.write(template)
    print(f"Day {day} created from template at {pypath.absolute()}")


def get_data_path(day: int):
    path = Path(f"./data/input{day}.txt")
    if not path.parent.is_dir():
        path.parent.mkdir()
    return path


def readlines(day: int):
    path = get_data_path(day)
    if not path.is_file():
        raise FileNotFoundError(f"File {path.absolute()} not found")
    with open(path) as f:
        return f.read().splitlines()


def write_input(day: int, data: str):
    path = get_data_path(day)
    with open(path, "w") as f:
        f.write(data)
    print(f"Input for day {day} written to {path.absolute()}")
