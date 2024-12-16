from datetime import datetime, timezone

import typer
from rich import print

from aoc.files import create_day_from_template, get_data_path, write_input
from aoc.leaderboard import fetch_leaderboard, print_daily_top_n
from aoc.requests import get_session

app = typer.Typer(no_args_is_help=True)


@app.command("lb")
def leaderboard(year: int = 2024, day: int = None, n: int = 3, board_id: int = 3239080):
    """Fetch the leaderboard

    Parameters
    ----------
    year : int
        The year to be used
    day : int
        Filter to a single day, prints all days if omitted
    n : int
        The number of top members to print
    board_id : int
        The ID of the leaderboard
    """
    data = fetch_leaderboard(year, board_id)
    print_daily_top_n(data, day=day, n=n)


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
