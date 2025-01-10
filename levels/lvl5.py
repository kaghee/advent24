import sys
import re
import math
from input_parsers import parse_input


EXAMPLE = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47\
"""

class PrintQueue:

    def __init__(self, input_file=None):
        self.pairs = []
        self.sequences = []
        self.correct_sequences = []
        self.input_file = input_file

    def find_relevant_pairs(self, seq):
        relevant_pairs = []
        for pair in self.pairs:
            if all(number in seq for number in pair.split("|")):
                relevant_pairs.append(pair)
        return relevant_pairs

    def run_first_task(self):
        """ For each update (sequence), finds the relevant ordering rules (pairs)
        and runs a RegEx search to check if the orders are right.
        """
        self.pairs, self.sequences = [line.split(
            "\n") for line in self.input_file.split("\n\n")]
        counter = 0
        correct_sequences = []

        for seq in self.sequences:
            valid = True

            relevant_pairs = self.find_relevant_pairs(seq)

            for p in relevant_pairs:
                first, second = p.split("|")
                if re.search(rf"{first}.*{second}", seq) is None:
                    valid = False

            if valid:
                correct_sequences.append(seq)
                middle = seq.split(",")[math.floor(len(seq.split(",")) / 2)]
                counter += int(middle)

        self.correct_sequences = correct_sequences
        print("Sum of middle numbers in correct sequences:", counter)

    def run_second_task(self):
        incorrect_sequences = list(
            set(self.sequences) - set(self.correct_sequences))
        # TODO: Complete second task
        pass


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    lines = EXAMPLE if use_example else parse_input('2024', '5')

    pq = PrintQueue(lines)
    print("Part I:")
    pq.run_first_task()

    print("\nPart II:")
    pq.run_second_task()
