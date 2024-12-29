#!/usr/bin/python3

import argparse
import sys
from levels import *


def run_level_on_input(input_str: str, example: bool = False):
    """ Runs the specified task on the respective puzzle input file. """
    level_no, task_no = input_str.split('-')  # e.g. 21-2
    file_name = f"{level_no}ex" if example else level_no

    app = sys.modules[f"levels.lvl{level_no}"]
    app.run_first_task(file_name) if task_no == "1" else app.run_second_task(file_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Specify which task to run and if it should use an example input source.")
    parser.add_argument("--source", required=True, type=str)
    parser.add_argument("-e", action="store_true", required=False)
    args = parser.parse_args()

    source = args.source
    example = args.e

    run_level_on_input(source, example)
