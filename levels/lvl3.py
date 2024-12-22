import re


def run_first_task(lines: list[str]):
    scores = 0
    for line in lines:
        matches = re.findall(r"mul\(\d{1,3},\d{1,3}\)", line)
        for item in matches:
            numbers = [int(x) for x in re.findall(r"\d+", item)]
            scores += numbers[0] * numbers[1]

    print(scores)


def run_second_task(lines: list[str]):
    scores = 0
    enabled = True
    for line in lines:
        matches = re.finditer(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", line)

        for item in [m.group() for m in matches]:
            numbers = [int(x) for x in re.findall(r"\d+", item)]
            if numbers and enabled:
                scores += numbers[0] * numbers[1]
            else:
                enabled = True if item == "do()" else False

    print(scores)
