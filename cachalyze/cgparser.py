"""
Cachegrind output file format:

    file         ::= desc_line* cmd_line events_line data_line+ summary_line
    desc_line    ::= 'desc:' ws? non_nl_string
    cmd_line     ::= 'cmd:' ws? cmd
    events_line  ::= 'events:' ws? (event ws)+
    data_line    ::= file_line | fn_line | count_line
    file_line    ::= 'fl=' filename
    fn_line      ::= 'fn=' fn_name
    count_line   ::= line_num ws? (count ws)+
    summary_line ::= 'summary:' ws? (count ws)+
    count        ::= num | '.'

Where:
    - non_nl_string is any string not containing a newline.
    - cmd is a string holding the command line of the profiled program.
    - event is a string containing no whitespace.
    - filename and fn_name are strings.
    - num and line_num are decimal numbers.
    - ws is whitespace.

"""
from cachalyze.cgcontainers import CGOutput, CGFile, CGFunction, CGLine, CGEvents


class CGParser:
    output = CGOutput()

    curr_file = None
    curr_function = None

    @staticmethod
    def read_count_line(line):
        return [int(i) for i in line.replace('.', '0').split(' ')]

    def cg_out_summary_line(self, line):
        counts = self.read_count_line(line)
        self.output.summary = CGEvents(*counts)

    def cg_out_count_line(self, line):
        counts = self.read_count_line(line)
        line = CGLine(*counts)
        self.curr_function.add_line(line)

    def cg_out_fn_line(self, line):
        function = CGFunction(self.curr_file, line)
        self.curr_file.add_function(function)
        self.curr_function = function

    def cg_out_file_line(self, line):
        file = CGFile(line)
        self.output.files.append(file)
        self.curr_file = file

    def cg_out_events_line(self, line):
        events = line.split(' ')
        self.output.events = events

    def cg_out_cmd_line(self, line):
        self.output.cmd = line

    def cg_out_desc_line(self, line):
        self.output.description.append(line)

    def handle_line(self, line):
        if line.startswith('#'):
            pass
        elif line.startswith('desc: '):
            self.cg_out_desc_line(line[5:])
        elif line.startswith('cmd: '):
            self.cg_out_cmd_line(line[4:])
        elif line.startswith('events: '):
            self.cg_out_events_line(line[8:])
        elif line.startswith('fl='):
            self.cg_out_file_line(line[3:])
        elif line.startswith('fn='):
            self.cg_out_fn_line(line[3:])
        elif line[0].isdigit():
            self.cg_out_count_line(line)
        elif line.startswith('summary: '):
            self.cg_out_summary_line(line[9:])
        else:
            self.output.unknown_lines.append(line)

    def parse(self, path):
        file = open(path, 'r')
        for line in file:
            self.handle_line(line.strip())
        file.close()

        self.output.verify()

        return self.output
