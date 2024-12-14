# Advent of Code

This repository contains solutions for the Advent of Code challenges.

## Getting Started

To get started with this project, you need to have `uv` [installed](https://docs.astral.sh/uv/getting-started/installation/).
With `uv` installed you can use `make sync` to create and synchronize a virtual environment with all the dependencies needed.

### How I Solved
To get started with I used `make setup` to install tools like `ipython` that I use for solving problems.

To prepare for a new puzzle I follow this process:
1. run `aoc create <day>` where `<day>` is the current puzzle number to solve. This uses `_template.py` to create a file that's ready for development with a few utilities like the `pr` function which makes copying answers easy.
2. Open a terminal and get ready with `aoc download <day>`, you'll be running this as soon as the puzzle drops
3. Open another terminal with `ipython` which you'll use for development. I mostly used the `%run dayXX.py` magic function to allow me to run scripts quickly but still have an interactive shell. By keeping code at the module-level after you use run you have access to all variables for further development.

## Available CLI Commands

The `aoc` package provides several CLI commands to help you manage and run your solutions. Below are the available commands:

- `aoc create <day>`: Initialize the solution for a specific day.
    ```sh
    aoc create 1
    ```

- `aoc download <day>`: Download the puzzle input to the `data/` directory for use in your script
    ```sh
    aoc download 1
    ```

- `aoc download-all`: Download all currently released puzzle inputs
    ```sh
    aoc download-all
    ```

- `aoc lb --day <day>`: print the top of the leaderboard for the given day filter (optional), shows actual submission times instead of just stars
    ```sh
    aoc lb --day 1
    ```

Use `aoc --help` for more information as all commands are documented and be sure to checkout all of the solution utilities like `aoc/grid.py`