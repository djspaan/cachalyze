import asyncio
import os

from cachalyze.cgparser import CGParser


class CGCacheConf:
    def __init__(self, size, assoc, line_size):
        self.size = size
        self.assoc = assoc
        self.line_size = line_size

    def __str__(self):
        return f'{self.size},{self.assoc},{self.line_size}'


class D1CacheConf(CGCacheConf):
    def __init__(self, size=32768, assoc=8, line_size=64):
        super().__init__(size, assoc, line_size)

    def get_cmd_option(self):
        return f'--D1={self.size},{self.assoc},{self.line_size}'


class LLCacheConf(CGCacheConf):
    def __init__(self, size=8388608, assoc=16, line_size=64):
        super().__init__(size, assoc, line_size)

    def get_cmd_option(self):
        return f'--LL={self.size},{self.assoc},{self.line_size}'


class CGRunConf:
    def __init__(self, program, d1=None, ll=None):
        self.program = program
        self.d1 = d1 or D1CacheConf()
        self.ll = ll or LLCacheConf()
        self.output_file = f'out/cgrunner.out.{self.program}.{self.d1}.{self.ll}'

    def get_cmd(self):
        cmd = 'valgrind --tool=cachegrind '
        cmd += f'--cachegrind-out-file={self.output_file}'
        cmd += f' {self.d1.get_cmd_option()}'
        cmd += f' {self.ll.get_cmd_option()}'
        cmd += f' data/sample_programs/{self.program}'
        return cmd


class CGRunner:
    def __init__(self, run_conf):
        self.run_conf = run_conf

    def run(self):
        os.system(self.run_conf.get_cmd())
        parser = CGParser(self.run_conf.output_file)
        return parser.parse()

    async def run_async_command(self):
        proc = await asyncio.create_subprocess_shell(
            self.run_conf.get_cmd(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc.communicate()

    async def run_async(self):
        await self.run_async_command()
        parser = CGParser(self.run_conf.output_file)
        return parser.parse()
