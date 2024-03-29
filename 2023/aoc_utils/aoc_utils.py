
def file_reader(file_path):
    """

    :param file_path: input file to read from
    :return: array of all file contents, no parsing or stripping occurs
    """
    all_lines = []
    with open(file_path, "r") as reader:
        all_lines = reader.readlines()

    return all_lines

def strip_newlines(line_list):
    return [x.rstrip("\n") for x in line_list]

def print_arr(a):
    s = ""
    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            if a[x][y] == 2:
                s += "O"
            elif a[x][y] == 1:
                s += "#"
            else:
                s+="."
        s += "\n"
    print(s)

