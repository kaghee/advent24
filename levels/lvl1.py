import collections

def get_lists(lines: list[str]):
    first_array = []
    second_array = []

    for line in lines:
        value_1, value_2 = line.split("   ")
        first_array.append(int(value_1))
        second_array.append(int(value_2))

    return first_array, second_array


def run_first_task(lines: list[str]):
    print("\nRunning level 1\n")
    
    diffs = 0
    first_array, second_array = get_lists(lines)

    while len(first_array):
        # Take the smallest number of the lists
        i, a = min(enumerate(first_array), key=lambda x: x[1])
        del first_array[i]
        i, b = min(enumerate(second_array), key=lambda x: x[1])
        del second_array[i]

        # Add their difference to the acc value
        curr = abs(a - b)
        diffs += curr

    print('sum of diffs:', diffs)
    

def run_second_task(lines: list[str]):
    print("\nRunning the second part of level 1\n")

    score = 0
    first_array, second_array = get_lists(lines)

    for curr in first_array:
        counter = collections.Counter(second_array)

        frequency = counter[curr]
        score += curr * frequency

    print('sum of frequencies:', score)
