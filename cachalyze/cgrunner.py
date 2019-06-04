import asyncio
import os

import cachalyze.config as config
from cachalyze.cgparser import CGParser


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
        self.output_file = f'out/cgrunner.out.{config.PROGRAM_ALIAS}.{self.d1}.{self.ll}'

    def get_cmd(self):
        cmd = 'valgrind --tool=callgrind --cache-sim=yes --compress-strings=no --compress-pos=no '
        cmd += f'--callgrind-out-file={self.output_file}'
        cmd += f' {self.d1.get_cmd_option()}'
        cmd += f' {self.ll.get_cmd_option()}'
        cmd += f' {config.PROGRAM_CMD}'
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
        # TODO: parse separately
        parser = CGParser(self.run_conf.output_file)
        return parser.parse()


class CGAsyncRunner:
    @staticmethod
    async def run_conf(conf):
        await CGRunner(conf).run_async()

    @staticmethod
    async def run_queue(loop):
        tasks = set()
        i = 0
        while i < len(RUN_CONFS):
            if len(tasks) >= config.N_THREADS:
                _done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            tasks.add(loop.create_task(CGAsyncRunner.run_conf(RUN_CONFS[i])))
            i += 1
        await asyncio.wait(tasks)

    @staticmethod
    def run():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.wait([CGAsyncRunner.run_queue(loop)]))
        loop.close()


RUN_CONFS = [
    *[CGRunConf(d1=CGD1CacheConf(size=i)) for i in config.CACHE_PARAMS['D1']['SIZE']],
    *[CGRunConf(d1=CGD1CacheConf(assoc=i)) for i in config.CACHE_PARAMS['D1']['ASSOC']],
    *[CGRunConf(d1=CGD1CacheConf(line_size=i)) for i in config.CACHE_PARAMS['D1']['LINE_SIZE']],
    *[CGRunConf(ll=CGLLCacheConf(size=i)) for i in config.CACHE_PARAMS['LL']['SIZE']],
    *[CGRunConf(ll=CGLLCacheConf(assoc=i)) for i in config.CACHE_PARAMS['LL']['ASSOC']],
    *[CGRunConf(ll=CGLLCacheConf(line_size=i)) for i in config.CACHE_PARAMS['LL']['LINE_SIZE']]
]
