# Reads data from the file.
def read_from_file(read_file):
    # The file is opened in read mode using the 'with' statement.
    with open(read_file, 'r') as file:
        # The contents of the file are read, stripped of leading and trailing whitespaces,
        # and stored in the variable `read_data`.
        read_data = file.read().strip()

        # The file is automatically closed upon exiting the 'with' block.
        file.close()

    # The read data is returned.
    return read_data
