import os
import re

from cachalyze.config import Config
from cachalyze.cgparser import CGParser
from cachalyze.cgrunner import CGD1CacheConf, CGLLCacheConf
from cachalyze.logger import Logger


class CGStorage:
    _cache = {}
    __instance = None
    DEFAULT_D1_CONF = f'{CGD1CacheConf.DEFAULT_SIZE},{CGD1CacheConf.DEFAULT_ASSOC},{CGD1CacheConf.DEFAULT_LINE_SIZE}'
    DEFAULT_LL_CONF = f'{CGLLCacheConf.DEFAULT_SIZE},{CGLLCacheConf.DEFAULT_ASSOC},{CGLLCacheConf.DEFAULT_LINE_SIZE}'

    def __new__(cls, **kwargs):
        if CGStorage.__instance is None:
            CGStorage.__instance = object.__new__(cls)
        return CGStorage.__instance

    def __init__(self):
        self.prefix = Config.OUT_PREFIX + r'\.' + Config.PROGRAM_ALIAS + r'\.'

    def parse(self, key):
        if key not in self._cache:
            self._cache[key] = CGParser(f'{Config.OUT_DIR}/{key}').parse()
            Logger.info(f'Successfully parsed output file {Config.OUT_DIR}/{key}')
        return self._cache[key]

    def get_regex(self, cache, param):
        params = Config.CACHE_PARAMS[cache][param]
        param_regex = "(" + "|".join(str(p) for p in params) + ")"
        regexes = {
            'D1': {
                'SIZE': self.prefix + param_regex + ',' + str(CGD1CacheConf.DEFAULT_ASSOC) + ','
                        + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF,
                'ASSOC': self.prefix + str(CGD1CacheConf.DEFAULT_SIZE) + ',' + param_regex + ','
                         + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF,
                'LINE_SIZE': self.prefix + str(CGD1CacheConf.DEFAULT_SIZE) + ','
                             + str(CGD1CacheConf.DEFAULT_ASSOC) + ',' + param_regex + r'\.' + self.DEFAULT_LL_CONF
            },
            'LL': {
                'SIZE': self.prefix + self.DEFAULT_D1_CONF + r'\.' + param_regex + ','
                        + str(CGLLCacheConf.DEFAULT_ASSOC) + r',' + str(CGLLCacheConf.DEFAULT_LINE_SIZE),
                'ASSOC': self.prefix + self.DEFAULT_D1_CONF + r'\.' + str(CGLLCacheConf.DEFAULT_SIZE)
                         + ',' + param_regex + ',' + str(CGLLCacheConf.DEFAULT_LINE_SIZE),
                'LINE_SIZE': self.prefix + self.DEFAULT_D1_CONF + r'\.' + str(CGLLCacheConf.DEFAULT_SIZE)
                             + r',' + str(CGLLCacheConf.DEFAULT_ASSOC) + ',' + param_regex
            }
        }
        return regexes[cache][param]

    def get_for_run_conf(self, rc):
        regex = self.prefix + str(rc.d1.size) + ',' + str(rc.d1.assoc) + ',' + str(rc.d1.line_size) + r'\.' \
                + str(rc.ll.size) + ',' + str(rc.ll.assoc) + ',' + str(rc.ll.line_size)

        for f in os.listdir(Config.OUT_DIR):
            if re.match(regex, f):
                return self.parse(f)

    def get_for_param(self, cache, param):
        outputs = []
        regex = self.get_regex(cache, param)

        for f in os.listdir(Config.OUT_DIR):
            if re.match(regex, f):
                outputs.append(self.parse(f))

        return sorted(outputs, key=lambda o: int(o.get_specs()[cache][param]))

    def get_for_program(self):
        outputs = []
        for f in os.listdir(Config.OUT_DIR):
            if re.match(self.prefix, f):
                outputs.append(self.parse(f))

        if not len(outputs):
            Logger.error('No output files found. Make sure that the --out-folder and --out-prefix options are '
                         'correctly set')

        return outputs
