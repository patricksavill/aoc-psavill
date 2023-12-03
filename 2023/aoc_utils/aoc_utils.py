
def file_reader(file_path):
    """

    :param file_path: input file to read from
    :return: array of all file contents, no parsing or stripping occurs
    """
    all_lines = []
    with open(file_path, "r") as reader:
        all_lines = reader.readlines()

    return all_lines
