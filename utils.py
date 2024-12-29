def get_file_content(file_name: str):
    input_path = f"inputs/{file_name}.txt"
    try:
        with open(input_path, "r") as f:
            print(f"Reading from {input_path}")
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {input_path}")


def get_file_lines(file_name: str):
    input_path = f"inputs/{file_name}.txt"
    try:
        with open(input_path, "r") as f:
            print(f"Reading from {input_path}")
            lines = [line.rstrip() for line in f]
            return lines
    except FileNotFoundError:
        print(f"File not found: {input_path}")
