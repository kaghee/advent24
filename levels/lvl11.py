import sys
import math
from input_parsers import parse_input


EXAMPLE = "125"
# EXAMPLE = "125 17"


class PlutonianPebbles:
    def __init__(self, pebbles):
        self.pebbles = pebbles
        self.pebbles_memo = {}

    def generate_pebbles(self, pebble):
        new_pebbles = []
        if pebble == 0:
            new_pebbles.append(1)
        elif not (math.floor(math.log10(pebble)) + 1) % 2:
            new_pebbles.append(int(str(pebble)[:len(str(pebble)) // 2]))
            new_pebbles.append(int(str(pebble)[len(str(pebble)) // 2:]))
        else:
            new_pebbles.append(pebble * 2024)

        return new_pebbles

    def visit(self, pebble):
        if pebble is None:
            return

    def get_generated_pebbles_after_n_blinks(self, pebble, count, repetitions, acc=None):
        if acc is None:
            acc = []

        pebbles = self.generate_pebbles(pebble)
        if count == repetitions:
            acc.extend(pebbles)
            return pebbles

        for peb in pebbles:
            self.get_generated_pebbles_after_n_blinks(
                peb, count + 1, repetitions, acc)

        return acc

    def run_task(self, repetitions):
        counter = 0
        for pebble in self.pebbles:
            res = self.get_generated_pebbles_after_n_blinks(
                pebble, 1, repetitions)
            counter += len(res)

        print("Number of pebbles:", counter)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '11')
    pebbles = [int(x) for x in input.split(" ")]

    print("Part I:")
    pp = PlutonianPebbles(pebbles)
    pp.run_task(25)

    print("Part II:")
    pp.run_task(35)
    # pp.run_task(pebbles, 50)
