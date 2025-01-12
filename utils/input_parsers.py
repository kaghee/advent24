from input_fetcher import fetch_input

def parse_input(year, day) -> str:
    """ Receives either the example input as a one item list,
    or the year and day as a two item list.
    Returns the parsed file. """
    input = fetch_input(year, day)
    return input

def get_lines(input: str) -> list[str]:
    return input.splitlines()

def get_line_chars_as_ints(input: str):
    return [list(map(int, list(l))) for l in input.splitlines()]

def get_line_chars(input: str):
    return [list(l) for l in input.splitlines()]
