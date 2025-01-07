import re
import itertools
import numpy as np
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

        self.antennas = antennas
        return antennas

    def is_on_map(self, x, y):
        return x >= 0 and y >= 0 and x < len(self.lines) and y < len(self.lines)

    def get_antinodes(self, pair, next_antinodes_only):
        """ Gets a pair of coordinates, determines the difference between their
        x and their y values, and generates the antinodes (or only the first antinode
        for Task 1) preceding the first element of the pair.
        Since this fnc runs on the result of itertools.permutations (as opposed to
        .combinations), `pairs` will include (a, b) and (b, a), so the antinodes
        will be generated before AND after the pair.
        """
        antinodes = []
        a, b = pair
        diff = [difference.item() for difference in tuple(np.subtract(b, a))]

        x, y = a
        if not next_antinodes_only:
            antinodes.append((x, y))
        while True:
            x -= diff[0]
            y -= diff[1]
            if self.is_on_map(x, y):
                antinodes.append((x, y))
                # We only need one set of coordinates for task 1
                if next_antinodes_only:
                    break
            else:
                break

        return antinodes


    def run_task(self, next_antinodes_only=False):
        antennas = self.get_antennas()
        antinodes = []
        for coords in antennas.values():
            # Get every pair combination of antennas for each frequency
            pairs = itertools.permutations(coords, 2)

            for pair in pairs:
                antinodes.extend(self.get_antinodes(pair, next_antinodes_only))

        print('Unique antinode locations:',len(set(antinodes)))


def run_first_task(file_name):
    lines = get_file_lines(file_name)
    ResonantCollinearity(lines).run_task(next_antinodes_only=True)

def run_second_task(file_name):
    lines = get_file_lines(file_name)
    ResonantCollinearity(lines).run_task()
