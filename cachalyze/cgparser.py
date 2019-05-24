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

from cachalyze.cgcontainers import CGOutput, CGFile, CGFunction, CGLine, CGEvents, CGObject


class CGParser:
    _curr_obj = None
    _curr_file = None
    _curr_func = None
    _curr_line = None

    def __init__(self, path):
        self.output = CGOutput()
        self.path = path

    def _read_count_line(self, line):
        return [int(i) for i in line.replace('.', '0').split(' ')]

    def cg_out_summary_line(self, line):
        counts = self._read_count_line(line)
        self.output.summary = CGEvents(*counts)

    def cg_out_count_line(self, line):
        counts = self._read_count_line(line)
        if not self._curr_line or counts[0] != self._curr_line.number:
            line = CGLine(*counts)
            self._curr_func.add_line(line)
            self._curr_line = line
        else:
            self._curr_line.add_counts(*counts[1:])

    def cg_out_fn_line(self, line):
        function = CGFunction(self._curr_file, line)
        self._curr_file.add_function(function)
        self._curr_func = function

    def cg_out_file_line(self, line):
        file = CGFile(line)
        self.output.files.append(file)
        self._curr_obj.files.append(file)
        self._curr_file = file

    def cg_out_obj_line(self, line):
        obj = CGObject(line)
        self.output.objects.append(obj)
        self._curr_obj = obj

    def cg_out_events_line(self, line):
        events = line.split(' ')
        self.output.events = events

    def cg_out_cmd_line(self, line):
        self.output.cmd = line

    def cg_out_desc_line(self, line):
        self.output.description.append(line.strip())

    def handle_line(self, line):
        if not len(line):
            pass
        elif line.startswith('#'):
            pass
        elif line.startswith('version:'):
            pass
        elif line.startswith('creator:'):
            pass
        elif line.startswith('pid:'):
            pass
        elif line.startswith('part:'):
            pass
        elif line.startswith('positions:'):
            pass
        elif line.startswith('calls='):
            pass
        elif line.startswith('fi='):
            pass
        elif line.startswith('fe='):
            pass
        elif line.startswith('cfn='):
            pass
        elif line.startswith('cob='):
            pass
        elif line.startswith('cfi='):
            pass
        elif line.startswith('desc: '):
            self.cg_out_desc_line(line[5:])
        elif line.startswith('cmd: '):
            self.cg_out_cmd_line(line[4:])
        elif line.startswith('events: '):
            self.cg_out_events_line(line[8:])
        elif line.startswith('ob='):
            self.cg_out_obj_line(line[3:])
        elif line.startswith('fl='):
            self.cg_out_file_line(line[3:])
        elif line.startswith('fn='):
            self.cg_out_fn_line(line[3:])
        elif line[0].isdigit():
            self.cg_out_count_line(line)
        elif line.startswith('summary: '):
            self.cg_out_summary_line(line[9:])
        elif line.startswith('totals: '):
            self.cg_out_summary_line(line[8:])
        else:
            self.output.unknown_lines.append(line)

    def parse(self):
        file = open(self.path, 'r')
        for line in file:
            self.handle_line(line.strip())
        file.close()

        return self.output
