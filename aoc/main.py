from datetime import datetime, timezone
import typer
from rich import print
from aoc.requests import get_session
from aoc.files import write_input, get_path

app = typer.Typer()


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
        path = get_path(day)
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
