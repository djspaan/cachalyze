import asyncio
import os

from cachalyze.config import Config
from cachalyze.cgparser import CGParser
from cachalyze.logger import Logger


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
        self.output_file = f'{Config.OUT_DIR}/{Config.OUT_PREFIX}.{Config.PROGRAM_ALIAS}.{self.d1}.{self.ll}'

    def get_cmd(self):
        cmd = 'valgrind --tool=callgrind --cache-sim=yes --compress-strings=no --compress-pos=no '
        cmd += f'--callgrind-out-file={self.output_file}'
        cmd += f' {self.d1.get_cmd_option()}'
        cmd += f' {self.ll.get_cmd_option()}'
        cmd += f' {Config.PROGRAM_CMD}'
        return cmd


class CGRunner:
    def __init__(self, run_conf):
        self.run_conf = run_conf

    def run(self):
        Logger.info(f'Starting simulation with parameters: {self.run_conf.d1.get_cmd_option()} '
                    f'{self.run_conf.ll.get_cmd_option()} (1/1)')
        os.system(self.run_conf.get_cmd())
        Logger.info(f'Simulation finished, writing results to: {self.run_conf.output_file} (1/1)')
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


class CGAsyncRunner:
    @staticmethod
    async def run_conf(conf, current=1, total=1):
        Logger.info(f'Starting simulation with parameters: {conf.d1.get_cmd_option()} '
                    f'{conf.ll.get_cmd_option()} ({current}/{total})')
        await CGRunner(conf).run_async()
        Logger.info(f'Simulation finished, writing results to: {conf.output_file} ({current}/{total})')

    @staticmethod
    async def run_queue(loop):
        tasks = set()
        run_confs = get_run_confs()
        print(len(run_confs))
        i = 0
        while i < len(run_confs):
            if len(tasks) >= Config.N_THREADS:
                _done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            tasks.add(loop.create_task(CGAsyncRunner.run_conf(run_confs[i], i + 1, len(run_confs))))
            i += 1
        await asyncio.wait(tasks)

    @staticmethod
    def run():
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.wait([CGAsyncRunner.run_queue(loop)]))
        loop.close()


def get_run_confs():
    """
    Get unique run configurations

    :return: [CGRunConf]
    """
    return [c for c in {c.output_file: c for c in [
        *[CGRunConf(d1=CGD1CacheConf(size=i)) for i in Config.CACHE_PARAMS['D1']['SIZE']],
        *[CGRunConf(d1=CGD1CacheConf(assoc=i)) for i in Config.CACHE_PARAMS['D1']['ASSOC']],
        *[CGRunConf(d1=CGD1CacheConf(line_size=i)) for i in Config.CACHE_PARAMS['D1']['LINE_SIZE']],
        *[CGRunConf(ll=CGLLCacheConf(size=i)) for i in Config.CACHE_PARAMS['LL']['SIZE']],
        *[CGRunConf(ll=CGLLCacheConf(assoc=i)) for i in Config.CACHE_PARAMS['LL']['ASSOC']],
        *[CGRunConf(ll=CGLLCacheConf(line_size=i)) for i in Config.CACHE_PARAMS['LL']['LINE_SIZE']]
    ]}.values()]
