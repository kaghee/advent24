from utils import get_file_lines


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


def run_first_task(file_name):
    lines = get_file_lines(file_name)
    BridgeRepair(lines).run_task()


def run_second_task(file_name):
    lines = get_file_lines(file_name)
    BridgeRepair(lines).run_task(with_concat=True)
