from utils import get_file_line_chars


class DiskFragmenter:
    def __init__(self, lines=None):
        self.disk_map = lines[0]
        self.visualized = []

    def transform(self):
        """ Transforms the input string into a list containing
        file blocks (represented by file id) and free spaces (None). """
        visualized = []
        for idx, char in enumerate(self.disk_map):
            file_id = None if idx % 2 else idx // 2
            visualized.extend([file_id] * int(char))

        assert len(visualized) == sum(map(int, self.disk_map)), "ERROR"
        self.visualized = visualized

    def move_blocks(self):
        """ For every free space, moves the last file block to occupy the space. """
        # Map uses steps by 2 as file blocks are the even numbers in the input
        no_of_files = sum(map(int, self.disk_map[0::2]))
        i = 0
        j = len(self.visualized) - 1
        while i < no_of_files:
            if self.visualized[i] is not None:
                i += 1
                continue
            while self.visualized[j] is None:
                j -= 1
            self.visualized[i] = self.visualized[j]
            self.visualized[j] = None
            i += 1

    def get_checksum(self):
        checksum = sum(
            [idx * item for idx, item in enumerate(self.visualized) if item is not None])
        return checksum

    def run_task(self):
        self.transform()
        self.move_blocks()
        print(f"The updated checksum is: {self.get_checksum()}")


def run_first_task(file_name):
    lines = get_file_line_chars(file_name)
    DiskFragmenter(lines).run_task()
