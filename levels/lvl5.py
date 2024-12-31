import re
import math
from utils import get_file_content


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


def run_first_task(file_name):
    input_file = get_file_content(file_name)
    PrintQueue(input_file).run_first_task()


def run_second_task(file_name):
    input_file = get_file_content(file_name)
    pq = PrintQueue(input_file)
    pq.run_first_task()
    pq.run_second_task()
