import sys
from input_parsers import parse_input, get_lines


EXAMPLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732\
"""

class HoofIt:
    def __init__(self, lines=None):
        self.disk_map = lines[0]
        self.visualized = []

    def run_task(self):
        pass


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '10')
    lines = get_lines(input)

    print("Part I:")
    hi = HoofIt(lines)
    hi.run_task(lines)

    # print("\nPart II:")
