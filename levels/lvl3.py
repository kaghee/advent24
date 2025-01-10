import re
import sys
from input_parsers import parse_input, get_lines


EXAMPLE = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


def run_first_task(lines):
    scores = 0
    for line in lines:
        matches = re.findall(r"mul\(\d{1,3},\d{1,3}\)", line)
        for item in matches:
            numbers = [int(x) for x in re.findall(r"\d+", item)]
            scores += numbers[0] * numbers[1]

    print(scores)


def run_second_task(lines):
    scores = 0
    enabled = True
    for line in lines:
        matches = re.finditer(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", line)

        for item in [m.group() for m in matches]:
            numbers = [int(x) for x in re.findall(r"\d+", item)]
            if numbers and enabled:
                scores += numbers[0] * numbers[1]
            else:
                enabled = True if item == "do()" else False

    print(scores)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '3')
    lines = get_lines(input)

    print("Part I:")
    run_first_task(lines)

    print("\nPart II:")
    run_second_task(lines)
