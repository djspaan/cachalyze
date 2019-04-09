def handle_line(line):
    print(line)


def parse(path):
    file = open(path, "r")

    for line in file:
        handle_line(line)

    file.close()