import sys
import collections
from input_parsers import parse_input, get_lines


EXAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3\
"""


def get_lists(lines: list[str]):
    first_array = []
    second_array = []

    for line in lines:
        value_1, value_2 = line.split("   ")
        first_array.append(int(value_1))
        second_array.append(int(value_2))

    return first_array, second_array


def run_first_task(lines):
    diffs = 0
    first_array, second_array = get_lists(lines)

    while len(first_array):
        # Take the smallest number of the lists
        i, a = min(enumerate(first_array), key=lambda x: x[1])
        del first_array[i]
        i, b = min(enumerate(second_array), key=lambda x: x[1])
        del second_array[i]

        # Add their difference to the acc value
        curr = abs(a - b)
        diffs += curr

    print('sum of diffs:', diffs)


def run_second_task(lines):
    score = 0
    first_array, second_array = get_lists(lines)

    for curr in first_array:
        counter = collections.Counter(second_array)

        frequency = counter[curr]
        score += curr * frequency

    print('sum of frequencies:', score)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '1')
    lines = get_lines(input)

    print("Part I:")
    run_first_task(lines)

    print("\nPart II:")
    run_second_task(lines)
