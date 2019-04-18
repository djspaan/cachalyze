import re


class CGOutput:
    def __init__(self):
        self.files = []
        self.description = []
        self.cmd = ''
        self.events = []
        self.summary = CGEvents()
        self.unknown_lines = []

    def get_specs(self):
        specs = {}
        for desc in self.description:
            m = re.match(r'^(I1|D1|LL) cache:[ ]+(\d+) B, (\d+) B, (\d+).+$', desc)
            if m:
                specs[m[1]] = {'size': m[2], 'line_size': m[3], 'assoc': m[4]}
        return specs

    def get_functions(self):
        return [function for file in self.files for function in file.functions.values()]

    def get_events(self):
        return self.events or self.calculate_events()

    def calculate_events(self):
        events = CGEvents()
        for file in self.files:
            for function in file.functions.values():
                events.add(function.events)
        return events

    def verify(self):
        self.verify_events()
        self.verify_count()

    def verify_events(self):
        for event in self.events:
            if event not in self.summary.__dict__:
                raise Exception(f'Event {event} not an attribute of CGEvents.')

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

    def get_lines_with_events(self):
        result = []
        self.get_content_lines()
        cglines = self.get_lines()
        for i, line in enumerate(self.content):
            line_events = CGEvents()
            line_cglines = list(filter(lambda l: l.number == i + 1, cglines))
            for cgline in line_cglines:
                line_events.add(cgline.events)
            result.append((i + 1, line, line_events))
        return result

    def get_content_lines(self):
        return self.content or self.read_content()

    def read_content(self):
        file = open(self.path, 'r')
        for line in file.readlines():
            self.content.append(line.rstrip())
        file.close()
        return self.content

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

    def get_formatted_name(self) -> str:
        return re.match(r'^(?:(?:^(?:/[^/]+)+)/|\?\?\?:)(.+)$', str(self))[1]

    def add_line(self, line):
        if line.number not in self.lines:
            self.lines[line.number] = line
        self.events.add(line.events)

    def merge(self, other):
        if str(self) != str(other):
            raise Exception(f'Merging of function {self} not possible with function {other}.')

        for line in other.lines:
            self.add_line(line)

    def __str__(self):
        return f'{self.file.path}:{self.name}'


class CGLine:
    def __init__(self, number, *args):
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

    @staticmethod
    def print_events():
        print('Ir I1mr ILmr Dr D1mr DLmr Dw D1mw DLmw')

    def add(self, events):
        for event in self.__dict__.keys():
            self.__dict__[event] += events.__dict__[event]

    def format(self, width=10):
        return '{:{width}} {:{width}} {:{width}} {:{width}} {:{width}} {:{width}} {:{width}} {:{width}} {:{width}}' \
            .format(self.Ir, self.I1mr, self.ILmr, self.Dr, self.D1mr, self.DLmr, self.Dw, self.D1mw, self.DLmw,
                    width=width, grouping=True)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return f'{self.Ir:,}  {self.I1mr:,}  {self.ILmr:,}  {self.Dr:,} \
         {self.D1mr:,}  {self.DLmr:,}  {self.Dw:,}  {self.D1mw:,}  {self.DLmw:,}'
