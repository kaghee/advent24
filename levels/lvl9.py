import re
from utils import get_file_line_chars

class DiskFragmenter:
    def __init__(self, lines=None):
        self.disk_map = lines[0]
        self.visualized = ""
        self.free_spaces = []

    def transform(self):
        visualized = ""
        free_spaces = []
        for idx, char in enumerate(self.disk_map):
            if idx % 2:
                # Odd indices mark blocks of free space. Add the correct number of
                # dots to the visualization and store their indices in a separate
                # list that will be used later for rearranging.
                free_spaces.extend(
                    list(range(len(visualized), len(visualized) + int(char))))
                # visualized += "." * int(char)
                visualized = "".join([visualized, "." * int(char)])
            else:
                # Even indices are files. Add them to the visualization by their file id.
                file_id = str(int(idx / 2))
                # visualized += file_id * int(char)
                visualized = "".join([visualized, file_id * int(char)])

        self.visualized = [char for char in visualized]
        self.free_spaces = free_spaces

    def move_blocks(self):
        # Iterate backwards through the visualized text.
        # Take the last digit to the first free space (and leave a space behind).
        for idx, char in enumerate(self.visualized[::-1]):
            # If the current char is a ".", no need to move blocks, so insert a dummy
            # item into free_spaces to preserve its indices for the file blocks.
            if char == ".":
                self.free_spaces.insert(idx, ".")
                self.visualized.pop()
                continue

            # Only proceed if there are still gaps with free space.
            if not re.search(r"\.", "".join(self.visualized)):
                break
            # Move the current char to the next available free space.
            self.visualized[self.free_spaces[idx]] = char
            self.visualized.pop()
            # print('index', "".join(self.visualized))

    def get_checksum(self):
        print("".join(self.visualized))
        checksum = 0
        for idx, char in enumerate(self.visualized):
            checksum += idx * int(char)
        return checksum


    def run_task(self):
        self.transform()
        print("Transform done")
        self.move_blocks()
        print("Moving blocks done")
        print(f"The updated checksum is: {self.get_checksum()}")

def run_first_task(file_name):
    lines = get_file_line_chars(file_name)
    DiskFragmenter(lines).run_task()
