class CGOutput:
    def __init__(self):
        self.files = []
        self.description = []
        self.cmd = ''
        self.events = []
        self.summary = CGEvents()

    def get_functions(self):
        return [function for file in self.files for function in file.functions.values()]

    def verify(self):
        self.verify_events()
        self.verify_count()

    def verify_events(self):
        for event in self.events:
            if event not in self.summary.__dict__:
                raise Exception('Event {} not an attribute of CGEvents.'.format(event))

    def verify_count(self):
        function_counts = CGEvents()
        line_counts = CGEvents()
        for file in self.files:
            for function in file.functions.values():
                function_counts.add(function.events)
                for line in function.lines.values():
                    line_counts.add(line.events)

        if not self.summary == function_counts == line_counts:
            raise Exception('Summarized counts not equal to parsed counts.')


class CGFile:
    def __init__(self, path):
        self.path = path
        self.functions = {}
        self.content = []

    def get_lines(self):
        return [l for f in self.functions for l in f.lines.values()]

    def get_content_lines(self):
        if self.content:
            return self.content
        self.read_content()
        return self.content

    def read_content(self):
        file = open(self.path, 'r')
        for line in file.readlines():
            self.content.append(line.rstrip())
        file.close()

    def add_function(self, function):
        if function in self.functions:
            self.functions[function].merge(function)
        else:
            self.functions[function] = function


class CGFunction:
    def __init__(self, file, name):
        self.file = file
        self.name = name
        self.lines = {}
        self.events = CGEvents()

    def add_line(self, line):
        if line.number not in self.lines:
            self.lines[line.number] = line
        self.events.add(line.events)

    def merge(self, other):
        if self.__str__() != other.__str__():
            raise Exception('Merging of function {} not possible with function {}.'.format(self, other))

        for line in other.lines:
            self.add_line(line)

    def __str__(self):
        return "{}:{}".format(self.file.path, self.name)


class CGLine:
    def __init__(self, file, function, number, *args):
        self.file = file
        self.function = function
        self.number = number
        self.events = CGEvents(*args)


class CGEvents:
    def __init__(self, Ir=0, I1mr=0, ILmr=0, Dr=0, D1mr=0, DLmr=0, Dw=0, D1mw=0, DLmw=0):
        self.Ir = Ir
        self.I1mr = I1mr
        self.ILmr = ILmr
        self.Dr = Dr
        self.D1mr = D1mr
        self.DLmr = DLmr
        self.Dw = Dw
        self.D1mw = D1mw
        self.DLmw = DLmw

    def add(self, events):
        self.Ir += events.Ir
        self.I1mr += events.I1mr
        self.ILmr += events.ILmr
        self.Dr += events.Dr
        self.D1mr += events.D1mr
        self.DLmr += events.DLmr
        self.Dw += events.Dw
        self.D1mw += events.D1mw
        self.DLmw += events.DLmw

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return '{} {} {} {} {} {} {} {} {}' \
            .format(self.Ir, self.I1mr, self.ILmr, self.Dr, self.D1mr, self.DLmr, self.Dw, self.D1mw, self.DLmw)
