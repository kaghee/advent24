import sys
from input_parsers import parse_input, get_line_chars_as_ints


# EXAMPLE = "0 1 10 99 999"
EXAMPLE = "125 17"


class PlutonianPebbles:
    def __init__(self, numbers: list[str]):
        self.pebbles = numbers
        self.updated = []

    def blink(self):
        i = 0
        while i < len(self.pebbles):
            pebble = self.pebbles[i]
            if pebble == "0":
                self.pebbles[i] = "1"
            elif not len(pebble) % 2:
                self.pebbles[i] = pebble[:len(pebble) // 2]
                self.pebbles.insert(i + 1, str(int(pebble[len(pebble) // 2:])))
                i += 1
            else:
                self.pebbles[i] = str(int(pebble) * 2024)
            i += 1

    def run_task(self, blinks):
        for _ in range(blinks):
            self.blink()
        print("Number of pebbles:", len(self.pebbles))


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '11')
    numbers = input.split(" ")
    # numbers = [(x, False) for x in input.split(" ")]

    print("Part I:")
    pp = PlutonianPebbles(numbers)
    pp.run_task(25)

    print("Part II:")
    pp.run_task(75)
