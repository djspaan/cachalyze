class CGOutput:
    def __init__(self, files=[], functions=[], lines=[], description=[], cmd='', events=[], summary=None):
        self.files = files
        self.functions = functions
        self.lines = lines
        self.description = description
        self.cmd = cmd
        self.events = events
        self.summary = summary if summary else CGEvents()

    def verify(self):
        return self.verify_events() and self.verify_count()

    def verify_count(self):
        counts = CGEvents()
        for line in self.lines:
            counts.add(line.events)

        if self.summary != counts:
            raise Exception('Summarized counts not equal to parsed counts.')

    def verify_events(self):
        for event in self.events:
            if event not in self.summary.__dict__:
                raise Exception('Event {} not an attribute of CGEvents.'.format(event))


class CGFile:
    def __init__(self, path, functions=[]):
        self.path = path
        self.functions = functions


class CGFunction:
    def __init__(self, file, name, lines=[]):
        self.file = file
        self.name = name
        self.lines = lines


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
