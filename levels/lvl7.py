import sys
from input_parsers import parse_input, get_lines


EXAMPLE = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20\
"""

class BridgeRepair:
    def __init__(self, lines=None):
        self.lines = lines

    def can_produce_value(self, value, base, rest_of_nums, with_concat=False):
        """ Takes a value, a base number and a list of numbers.
        It returns True if value can be obtained by adding, multiplying
        and optionally even concatenating the base number with the next
        in the rest of the numbers."""
        is_valid_1 = False
        is_valid_2 = False
        is_valid_3 = False

        if not rest_of_nums:
            return base == value

        acc_1 = base + rest_of_nums[0]  # Addition
        acc_2 = base * rest_of_nums[0]  # Multiplication
        acc_3 = int(f"{base}{rest_of_nums[0]}")     # Concatenation

        if acc_1 <= value:
            is_valid_1 = self.can_produce_value(
                value, acc_1, rest_of_nums[1:], with_concat=with_concat)
        if acc_2 <= value:
            is_valid_2 = self.can_produce_value(
                value, acc_2, rest_of_nums[1:], with_concat=with_concat)
        if acc_3 <= value:
            is_valid_3 = self.can_produce_value(
                value, acc_3, rest_of_nums[1:], with_concat=with_concat)

        if with_concat:
            return is_valid_1 or is_valid_2 or is_valid_3
        else:
            return is_valid_1 or is_valid_2

    def run_task(self, with_concat=False):
        counter = 0
        for line in self.lines:
            value, numbers = int(
                line[:line.index(":")]), line[line.index(":") + 2:]
            numbers = [int(n) for n in numbers.split(" ")]

            if self.can_produce_value(value, numbers[0], numbers[1:], with_concat):
                counter += value

        print("Result:", counter)


if __name__ == "__main__":
    use_example = "-e" in sys.argv

    input = EXAMPLE if use_example else parse_input('2024', '7')
    lines = get_lines(input)

    br = BridgeRepair(lines)
    print("Part I:")
    br.run_task()

    print("\nPart II:")
    br.run_task(with_concat=True)
