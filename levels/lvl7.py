from utils import get_file_lines


class BridgeRepair:
    def __init__(self, lines=None):
        self.lines = lines

    def process_next_num(self, value, base, rest_of_nums):
        is_valid_1 = False
        is_valid_2 = False

        if not rest_of_nums:
            return base == value
        acc_1 = base + rest_of_nums[0]
        acc_2 = base * rest_of_nums[0]
        if acc_1 <= value:
            is_valid_1 = self.process_next_num(value, acc_1, rest_of_nums[1:])
        if acc_2 <= value:
            is_valid_2 = self.process_next_num(value, acc_2, rest_of_nums[1:])

        return is_valid_1 or is_valid_2

    def run_first_task(self):
        counter = 0
        for line in self.lines:
            print(line)
            value, numbers = int(
                line[:line.index(":")]), line[line.index(":") + 2:]
            numbers = [int(n) for n in numbers.split(" ")]

            if self.process_next_num(value, numbers[0], numbers[1:]):
                counter += value

        print("Result:", counter)


def run_first_task(file_name):
    lines = get_file_lines(file_name)

    BridgeRepair(lines).run_first_task()

