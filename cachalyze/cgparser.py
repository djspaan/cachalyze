from cachalyze.cgcontainers import CGOutput, CGFile, CGFunction, CGLine, CGEvents, CGObject


class CGParser:
    def __init__(self, path):
        self._curr_obj = CGObject('undefined')
        self._curr_file = CGFile('undefined')
        self._curr_obj.files.append(self._curr_file)
        self._curr_func = CGFunction(self._curr_file, 'undefined')
        self._curr_file.add_func(self._curr_func)
        self._curr_line = None
        self._curr_cfile = CGFile('undefined')
        self.output = CGOutput()
        self.output.objects.append(self._curr_obj)
        self.output.files.append(self._curr_file)
        self.path = path

    def _read_count_line(self, line):
        return [int(i) for i in line.replace('.', '0').split()]

    def cg_out_summary_line(self, line):
        counts = self._read_count_line(line)
        self.output.summary = CGEvents(*counts)

    def cg_out_count_line(self, line):
        counts = self._read_count_line(line)
        line = CGLine(*counts)
        self._curr_func.add_line(line)
        self._curr_line = line

    def cg_out_fn_line(self, line):
        func = CGFunction(self._curr_file, line)
        func = self._curr_file.add_func(func)
        self._curr_func = func

    def cg_out_cfn_line(self, line):
        self._curr_func.callees.add(str(CGFunction(self._curr_cfile, line)))

    def cg_out_cfi_line(self, line):
        self._curr_cfile = CGFile(line)

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
            self.cg_out_cfn_line(line[4:])
        elif line.startswith('cob='):
            pass
        elif line.startswith('cfi='):
            self.cg_out_cfi_line(line[4:])
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

