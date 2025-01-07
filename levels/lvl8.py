import re
import itertools
from utils import get_file_lines


class ResonantCollinearity:
    def __init__(self, lines=None):
        self.lines = lines
        self.antennas = dict()

    def get_antennas(self):
        """ Collects sets of coordinates for every antenna in each frequency. """
        antennas = dict()
        for row, line in enumerate(self.lines):
            matches = re.finditer(r"[^\.]", line)
            for match in matches:
                if match.group() not in antennas:
                    antennas[match.group()] = [(row, match.start())]
                else:
                    antennas[match.group()].append((row, match.start()))

        return antennas

    def get_antinodes(self, pair):
        a, b = pair

        anti_1 = (a[0] + (a[0] - b[0]), a[1] + (a[1] - b[1]))
        anti_2 = (b[0] + (b[0] - a[0]), b[1] + (b[1] - a[1]))

        # Throw away any antinode whose coordinates are off the map
        valid_antinodes = [node for node in [anti_1, anti_2] if all(
            coord >= 0 and coord < len(self.lines) for coord in node)]

        return valid_antinodes

    def run_task(self):
        antennas = self.get_antennas()
        antinodes = []
        for coords in antennas.values():
            # Get every pair combination of antennas for each frequency
            pairs = itertools.combinations(coords, 2)

            for pair in pairs:
                antinodes.extend(self.get_antinodes(pair))

        print('Unique antinode locations:',len(set(antinodes)))


def run_first_task(file_name):
    lines = get_file_lines(file_name)
    ResonantCollinearity(lines).run_task()
