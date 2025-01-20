import sys
import re
from input_parsers import parse_input
from sympy import symbols, Eq, solve
from sympy.core.numbers import Integer as SympyInteger


EXAMPLE = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279\
"""


class ClawContraption:
    def __init__(self, machines):
        self.machines = machines

    def get_coords(self, machine: str):
        nums = [int(m.group()) for m in re.finditer(r"\d+", machine)]
        return nums

    def get_winner_tokens(self, coords: list[int], with_correction: bool = False):
        a_x, a_y, b_x, b_y, prize_x, prize_y = coords

        if with_correction:
            prize_x += 10000000000000
            prize_y += 10000000000000

        k, j = symbols('k j')
        eq1 = Eq(a_x * k + b_x * j, prize_x)
        eq2 = Eq(a_y * k + b_y * j, prize_y)

        result = solve((eq1, eq2), (k, j))

        # If the result is a fraction, we don't need it
        if isinstance(result[k], SympyInteger) and isinstance(result[j], SympyInteger):
            return result[k] * 3 + result[j]
        else:
            return 0

    def run_task(self, with_correction: bool = False):
        tokens = 0
        for machine in self.machines:
            coords = self.get_coords(machine)
            tokens += self.get_winner_tokens(coords, with_correction)

        return tokens


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '13')
    machines = input.split("\n\n")

    print("Part I:")
    cc = ClawContraption(machines)
    tokens = cc.run_task()
    print("Tokens needed:", tokens)

    print("Part II:")
    tokens = cc.run_task(with_correction=True)
    print("Tokens needed after correction:", tokens)
