import sys
from input_parsers import parse_input, get_lines


EXAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9\
"""


def is_negative(num: int):
    return num < 0


def is_report_safe(report) -> bool:
    diffs = []

    for idx, value in enumerate(report[:-1]):
        diffs.append(value - report[idx+1])

    if any(abs(diff) > 3 or diff == 0 for diff in diffs):
        return False

    if len(set([is_negative(diff) for diff in diffs])) > 1:
        return False

    return True


def is_almost_safe(report):
    for idx, _ in enumerate(report):
        new_report = report.copy()
        del new_report[idx]
        is_safe = is_report_safe(new_report)
        if is_safe:
            return True

    return False


def run_first_task(lines):
    counter = 0
    for line in lines:
        report = [int(x) for x in line.split(" ")]
        if is_report_safe(report):
            counter += 1

    print('counter', counter)


def run_second_task(lines):
    counter = 0
    unsafe_reports = []

    for line in lines:
        report = [int(x) for x in line.split(" ")]
        if is_report_safe(report):
            counter += 1
        else:
            unsafe_reports.append(report)

    print('counter', counter)

    for report in unsafe_reports:
        if is_almost_safe(report):
            counter += 1

    print('final counter', counter)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '2')
    lines = get_lines(input)

    print("Part I:")
    run_first_task(lines)

    print("\nPart II:")
    run_second_task(lines)
