import importlib.util
import sys
from datetime import datetime, timezone

import typer
from rich import print

from aoc.files import create_day_from_template, get_data_path, get_py_path, write_input
from aoc.requests import get_session

app = typer.Typer()


@app.command()
def run(day: int, year: int = 2024):
    """Run the solution for a given day

    Parameters
    ----------
    day : int
        The day to be run
    """
    script_file = get_py_path(day)
    if not script_file.is_file():
        print(f"Day {day} has not been implemented yet")
        return

    spec = importlib.util.spec_from_file_location(script_file.stem, script_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[script_file.stem] = module
    spec.loader.exec_module(module)
    try:
        module.part_one()
        module.part_two()
    except AttributeError:
        print("The module does not have part_one or part_two functions")


@app.command()
def create(day: int):
    """Create a new day from the template

    Parameters
    ----------
    day : int
        The day to be created
    """
    create_day_from_template(day)


@app.command()
def download_all(year: int = 2024):
    """Download the input for a given day

    Parameters
    ----------
    year : int
        The year to be used
    """
    now = datetime.now(timezone.utc)
    this_year = now.date().year
    max_day = 25
    if year == this_year:
        max_day = now.date().day

    print(f"Downloading all inputs for year {year} through day {max_day}")
    for day in range(1, max_day + 1):
        path = get_data_path(day)
        if path.is_file():
            print(f"Input for day {day} already exists at {path.absolute()}")
            continue
        download(day, year)


@app.command()
def download(day: int, year: int = 2024):
    """Download the input for a given day

    Parameters
    ----------
    day : int
        The day to be downloaded
    """
    # The user needs to have setup a session cookie
    # in the environment variable AOC_SESSION
    session = get_session()
    response = session.get(f"https://adventofcode.com/{year}/day/{day}/input")
    response.raise_for_status()
    print(f"Input for day {year}/{day} downloaded")
    write_input(day, response.text)
