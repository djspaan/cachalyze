import os
import time

from cachalyze.cgparser import CGParser


class CGRunner:
    def __init__(self, program, options=[]):
        self.program = program
        self.options = options
        self.output_file = 'out/cgrunner.out.' + str(time.time())

    def get_cmd(self):
        cmd = "valgrind --tool=cachegrind "
        cmd += ' '.join(self.options)
        cmd += ' ' + self.program
        return cmd

    def run(self):
        self.options.append('--cachegrind-out-file=' + self.output_file)
        os.system(self.get_cmd())
        parser = CGParser(self.output_file)
        return parser.parse()
