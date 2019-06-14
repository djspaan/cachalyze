import re


class CGOutput:
    def __init__(self):
        self.objects = []
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
                specs[m[1]] = {'SIZE': m[2], 'LINE_SIZE': m[3], 'ASSOC': m[4]}
        return specs

    def get_funcs(self):
        return [function for file in self.files for function in file.functions.values()]

    def get_func(self, func):
        funcs = self.get_funcs()
        for f in funcs:
            if str(f) == func:
                return f

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
        for file in self.files:
            for function in file.functions.values():
                function_counts.add(function.events)

        if not self.summary == function_counts:
            raise Exception('Summarized counts not equal to parsed counts.')


class CGObject:
    def __init__(self, name):
        self.name = name
        self.files = []


class CGFile:
    def __init__(self, path):
        self.path = path
        self.functions = {}
        self.content = []

    def get_lines(self):
        return [l for f in self.functions.values() for l in f.lines.values()]

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

    def add_func(self, func):
        if str(func) in self.functions:
            self.functions[str(func)].merge(func)
            return self.functions[str(func)]
        else:
            self.functions[str(func)] = func
            return func


class CGFunction:
    def __init__(self, file, name):
        self.file = file
        self.name = name
        self.lines = {}
        self.callees = set()
        self.events = CGEvents()

    def get_formatted_name(self) -> str:
        return re.match(r'^(?:(?:^(?:/[^/]+)+)/|\?\?\?:)(.+)$', str(self))[1]

    def add_line(self, line):
        if line.number not in self.lines:
            self.lines[line.number] = line
        else:
            self.lines[line.number].events.add(line.events)
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
    def __init__(self, Ir=0, Dr=0, Dw=0, I1mr=0, D1mr=0, D1mw=0, ILmr=0, DLmr=0, DLmw=0):
        self.Ir = Ir
        self.Dr = Dr
        self.Dw = Dw
        self.I1mr = I1mr
        self.D1mr = D1mr
        self.D1mw = D1mw
        self.ILmr = ILmr
        self.DLmr = DLmr
        self.DLmw = DLmw

    def add(self, events):
        self.Ir += events.Ir
        self.Dr += events.Dr
        self.Dw += events.Dw
        self.I1mr += events.I1mr
        self.D1mr += events.D1mr
        self.D1mw += events.D1mw
        self.ILmr += events.ILmr
        self.DLmr += events.DLmr
        self.DLmw += events.DLmw

    # def add(self, events):
    #     self.Ir = self.Ir + events.Ir
    #     self.Dr = self.Dr + events.Dr
    #     self.Dw = self.Dw + events.Dw
    #     self.I1mr = self.I1mr + events.I1mr
    #     self.D1mr = self.D1mr + events.D1mr
    #     self.D1mw = self.D1mw + events.D1mw
    #     self.ILmr = self.ILmr + events.ILmr
    #     self.DLmr = self.DLmr + events.DLmr
    #     self.DLmw = self.DLmw + events.DLmw

    # def add(self, events):
    #     for event in self.__dict__.keys():
    #         self.__dict__[event] += events.__dict__[event]

    def format(self):
        return '{:,} & {:,} & {:,} & {:,} & {:,} & {:,} & {:,} & {:,} & {:,}' \
            .format(self.Ir, self.Dr, self.Dw, self.I1mr, self.D1mr, self.D1mw, self.ILmr, self.DLmr, self.DLmw)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return f'Ir:{self.Ir:,}  Dr:{self.Dr:,}  Dw:{self.Dw:,}  I1mr:{self.I1mr:,} D1mr:{self.D1mr:,}  D1mw:{self.D1mw:,}  ILmr:{self.ILmr:,}  DLmr:{self.DLmr:,}  DLmw:{self.DLmw:,}'
