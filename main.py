#!/usr/bin/python3

import argparse
import sys
from levels import *


def get_file_content(input_path: str):
    with open(input_path, "r") as f:
        print(f"Reading from {input_path}")
        lines = [line.rstrip() for line in f]
        return lines


def load_input(file_name: str):
    """ Loads a file for the given level.  """
    input_path = f"inputs/{file_name}.txt"
    try:
        return get_file_content(input_path)
    except FileNotFoundError:
        print(f"File not found: {input_path}")


def run_level_on_input(input_str: str, example: bool = False):
    """ Runs the specified task on the respective puzzle input file. """
    level_no, task_no = input_str.split('-')  # e.g. 21-2
    lines = load_input(f"{level_no}ex") if example else load_input(level_no)

    app = sys.modules[f"levels.lvl{level_no}"]
    app.run_first_task(lines) if task_no == "1" else app.run_second_task(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Specify which task to run and if it should use an example input source.")
    parser.add_argument("--source", required=True, type=str)
    parser.add_argument("-e", action="store_true", required=False)
    args = parser.parse_args()

    source = args.source
    example = args.e

    run_level_on_input(source, example)
