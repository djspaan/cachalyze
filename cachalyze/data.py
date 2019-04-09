class File:
    def __init__(self, path):
        self.path = path

class Function:
    def __init__(self, file, name, lines):
        self.file = file
        self.name = name
        self.lines = []

class Line:
    def __init__(self, file, number, content):
        self.file = file
        self.number = number
        self.content = content