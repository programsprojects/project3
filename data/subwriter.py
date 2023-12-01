# Writes data to the file.
def write_to_file(file, data):
    # The file is opened in write mode using the 'with' statement.
    with open(file, 'w') as file:
        # The provided data is written to the file, followed by a newline character.
        file.write(data + "\n")

        # The file is automatically closed upon exiting the 'with' block.
        file.close()
