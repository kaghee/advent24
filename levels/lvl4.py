import re
import numpy as np
from utils import get_file_lines


def rotate_matrix(matrix):
    return np.rot90(matrix)


def count_occurrences(lines):
    counter = 0
    for row in lines:
        counter += len(re.findall(r"(?=XMAS|SAMX)", "".join(row)))
    return counter


def run_first_task(file_name):
    lines = get_file_lines(file_name)

    counter = 0

    # Horizontal
    counter += count_occurrences(lines)

    # Vertical
    verticals = rotate_matrix([list(line) for line in lines])
    counter += count_occurrences(verticals)

    # Diagonal
    a = np.array([list(line) for line in lines])

    diagonal_lines = [a[::-1, :].diagonal(i)
                      for i in range(-a.shape[0]+1, a.shape[1])]
    diagonal_lines.extend(a.diagonal(i)
                          for i in range(a.shape[1]-1, -a.shape[0], -1))
    diagonals = ["".join(line.tolist()) for line in diagonal_lines]

    counter += count_occurrences(diagonals)

    print("Total occurrences:", counter)


def is_valid_cross(lines: list[str], ctr: list[int]) -> bool:
    top_left = lines[ctr[0] - 1][ctr[1] - 1]
    bot_right = lines[ctr[0] + 1][ctr[1] + 1]

    if not re.search(r"MAS|SAM", f"{top_left}A{bot_right}"):
        return False

    top_right = lines[ctr[0] - 1][ctr[1] + 1]
    bot_left = lines[ctr[0] + 1][ctr[1] - 1]

    if not re.match(r"MAS|SAM", f"{top_right}A{bot_left}"):
        return False

    return True


def run_second_task(file_name):
    lines = get_file_lines(file_name)

    """ Iterates through the text leaving the edges off.
    For each possible cross center ('A'), checks if the letters
    in the cross are valid or not. """
    counter = 0

    for idx, row in enumerate(lines[1:-1]):
        matches = re.finditer(r"A", row[1:-1])
        # Store centres as Y, Z coordinates
        centres = [[idx + 1, m.span()[0] + 1] for m in matches]
        for ctr in centres:
            counter += is_valid_cross(lines, ctr)

    print("Number of crosses:", counter)
