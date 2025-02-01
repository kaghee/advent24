import re
import sys
import math
from input_parsers import get_lines, parse_input
from enum import Enum


EXAMPLE = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0\
"""

EXAMPLE = """\
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0\
"""

class OperandType(Enum):
    LITERAL = "lit"
    COMBO = "combo"


class ChronospatialComputer:

    def __init__(self, registers, program):
        self.INSTRUCTIONS = {
            0: ["adv", OperandType.COMBO],
            1: ["bxl", OperandType.LITERAL],
            2: ["bst", OperandType.COMBO],
            3: ["jnz", OperandType.LITERAL],
            4: ["bxc", None],
            5: ["out", OperandType.COMBO],
            6: ["bdv", OperandType.COMBO],
            7: ["cdv", OperandType.COMBO],
        }
        self.register_a, self.register_b, self.register_c = registers
        self.program = program
        self.operand_type = None
        self.output = ""

    def get_operand_value(self, instruction, operand):
        if instruction[1] == OperandType.LITERAL:
            return operand

        if 0 <= operand <= 3:
            return operand

        if operand == 4:
            return self.register_a

        if operand == 5:
            return self.register_b

        if operand == 6:
            return self.register_c

    def adv(self, operand):
        denominator = 2 ** operand
        self.register_a = math.trunc(self.register_a / denominator)

    def bxl(self, operand):
        """ Sets register B to register B bitwise XOR literal operand. """
        self.register_b = self.register_b ^ operand

    def bst(self, operand):
        self.register_b = operand % 8

    def jnz(self, operand):
        if self.register_a == 0:
            return None
        return operand, None

    def bxc(self, operand):
        self.register_b = self.register_b ^ self.register_c

    def out(self, operand):
        return None, operand % 8

    def bdv(self, operand):
        denominator = 2 ** operand
        self.register_b = math.trunc(self.register_a / denominator)

    def cdv(self, operand):
        denominator = 2 ** operand
        self.register_c = math.trunc(self.register_a / denominator)

    def run_task(self):
        i = 0
        while len(self.program) > i:
            if i % 2:
                i += 1
                continue

            instruction = self.program[i]
            argument = self.program[i + 1]

            func = getattr(self, self.INSTRUCTIONS[instruction][0])
            operand = self.get_operand_value(
                self.INSTRUCTIONS[instruction], argument)
            result = func(operand)

            if result is not None:
                pointer, output = result
                if output is not None:
                    self.output += f"{output},"
                    i += 1
                if pointer is not None:
                    i = pointer
            else:
                i += 1

        # print("A:", self.register_a)
        print("Output of the program:", self.output)

if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '17')

    lines = get_lines(input)

    registers = [int(re.search(r"\d+", register).group())
                 for register in lines[:lines.index("")]]
    program = [int(instr) for instr in lines[-1].split(" ")[1].split(",")]

    print("Part I:")
    cc = ChronospatialComputer(registers, program)
    cc.run_task()
