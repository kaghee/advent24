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

    def get_files_and_spaces(self):
        """ Creates two lists of tuples, storing the index and size of
        each block for files and for free spaces. """
        files = []
        free_slots = []
        curr_index = 0
        for idx, char in enumerate(self.disk_map):
            if idx % 2:
                free_slots.append((curr_index, int(char)))
            else:
                files.append(int(char))

            curr_index += int(char)
        return files, free_slots

    def move_blocks(self):
        """ For every free space, moves the last file block to occupy the space. """
        # Map uses steps by 2 as file blocks are the even numbers in the input
        no_of_file_blocks = sum(map(int, self.disk_map[0::2]))
        i = 0
        j = len(self.visualized) - 1
        while i < no_of_file_blocks:
            if self.visualized[i] is not None:
                i += 1
                continue
            while self.visualized[j] is None:
                j -= 1
            self.visualized[i] = self.visualized[j]
            self.visualized[j] = None
            i += 1

    def move_files(self):
        files, free_slots = self.get_files_and_spaces()
        i = 0
        j = len(self.visualized) - 1
        # While there are file blocks left to move
        while len(files):
            # Take the rightmost file block
            file_size = files.pop()

            # Find the first possible free slot (left of j) for a file this big
            slot_data = next(([idx, x] for idx, x in enumerate(
                free_slots) if x[1] >= file_size and x[0] < j), None)

            # If no such slot exists, skip the file block: move j left by file_size
            if slot_data is None:
                j -= file_size

            else:
                slot_id, slot = slot_data
                # If a slot exists, bring i to the index of the slot
                i = slot[0]
                curr_file_id = len(files)
                # If j is on an empty space, move to the next block.
                # If j is on a number bigger than itself, it means that number
                # has already been moved, so should not be touched: move to the next block.
                while self.visualized[j] is None or self.visualized[j] > curr_file_id:
                    j -= 1
                # Fill up the slot with the current file block and remove the file from its original position
                for k in range(file_size):
                    self.visualized[i + k] = curr_file_id
                    self.visualized[j - k] = None

                # If the slot was == the file_size, remove the slot item from free_slots
                if slot[1] == file_size:
                    free_slots.remove(slot)
                # If the slot was bigger, update the slot item to its new index and length
                # after having filled it partially
                else:
                    free_slots[slot_id] = (
                        slot[0] + file_size, slot[1] - file_size)

    def get_checksum(self):
        checksum = sum(
            [idx * item for idx, item in enumerate(self.visualized) if item is not None])
        return checksum

    def run_task(self, whole_files=False):
        self.transform()
        if whole_files:
            self.move_files()
        else:
            self.move_blocks()
        print(f"The updated checksum is: {self.get_checksum()}")


def run_first_task(file_name):
    lines = get_file_line_chars(file_name)
    DiskFragmenter(lines).run_task()


def run_second_task(file_name):
    lines = get_file_line_chars(file_name)
    DiskFragmenter(lines).run_task(whole_files=True)
