import asyncio
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

    async def run_command(self):
        proc = await asyncio.create_subprocess_shell(self.get_cmd(), stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)
        await proc.communicate()

    async def run(self):
        self.options.append('--cachegrind-out-file=' + self.output_file)
        await self.run_command()
        parser = CGParser(self.output_file)
        return parser.parse()
