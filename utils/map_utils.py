def visualize(map_):
    print("\n\n")
    for line in map_:
        print("".join([str(x) for x in line]))

def is_on_map(map_, coord: tuple[int, int]) -> bool:
    return 0 <= coord[0] < len(map_) and 0 <= coord[1] < len(map_[0])
