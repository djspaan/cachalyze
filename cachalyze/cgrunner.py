import asyncio
import os

from cachalyze.cgparser import CGParser

# PROGRAM_CMD = 'data/sample_programs/bad_cacher'
# PROGRAM_CMD = 'timeout 5m /home/dennisspaan/Workspace/hub/build/local_subscriber/local_subscriber -s -c \
#                     /home/dennisspaan/Workspace/hub/conf/local_subscriber.xml'
PROGRAM_CMD = '/home/dennisspaan/Workspace/test/bld/app/test -s -c \
              /home/dennisspaan/Workspace/test/bld/app/test.xml'
PROGRAM_ALIAS = 'test'


class CGCacheConf:
    def __init__(self, size, assoc, line_size):
        self.size = size
        self.assoc = assoc
        self.line_size = line_size

    def __str__(self):
        return f'{self.size},{self.assoc},{self.line_size}'


class CGD1CacheConf(CGCacheConf):
    DEFAULT_SIZE = 32768
    DEFAULT_ASSOC = 8
    DEFAULT_LINE_SIZE = 64

    def __init__(self, size=DEFAULT_SIZE, assoc=DEFAULT_ASSOC, line_size=DEFAULT_LINE_SIZE):
        super().__init__(size, assoc, line_size)

    def get_cmd_option(self):
        return f'--D1={self.size},{self.assoc},{self.line_size}'


class CGLLCacheConf(CGCacheConf):
    DEFAULT_SIZE = 8388608
    DEFAULT_ASSOC = 16
    DEFAULT_LINE_SIZE = 64

    def __init__(self, size=DEFAULT_SIZE, assoc=DEFAULT_ASSOC, line_size=DEFAULT_LINE_SIZE):
        super().__init__(size, assoc, line_size)

    def get_cmd_option(self):
        return f'--LL={self.size},{self.assoc},{self.line_size}'


class CGRunConf:
    def __init__(self, d1=None, ll=None):
        self.d1 = d1 or CGD1CacheConf()
        self.ll = ll or CGLLCacheConf()
        self.output_file = f'out/cgrunner.out.{PROGRAM_ALIAS}.{self.d1}.{self.ll}'

    def get_cmd(self):
        cmd = 'valgrind --tool=cachegrind '
        cmd += f'--cachegrind-out-file={self.output_file}'
        cmd += f' {self.d1.get_cmd_option()}'
        cmd += f' {self.ll.get_cmd_option()}'
        cmd += f' {PROGRAM_CMD}'
        return cmd


class CGRunner:
    def __init__(self, run_conf):
        self.run_conf = run_conf

    def run(self):
        os.system(self.run_conf.get_cmd())
        parser = CGParser(self.run_conf.output_file)
        return parser.parse()

    async def run_async_cmd(self):
        proc = await asyncio.create_subprocess_shell(
            self.run_conf.get_cmd(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc.communicate()

    async def run_async(self):
        await self.run_async_cmd()
        parser = CGParser(self.run_conf.output_file)
        return parser.parse()
