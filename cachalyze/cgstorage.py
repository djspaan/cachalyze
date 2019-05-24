import os
import re

from cachalyze import config
from cachalyze.cgparser import CGParser
from cachalyze.cgrunner import CGD1CacheConf, CGLLCacheConf


class CGStorage:
    DEFAULT_D1_CONF = f'{CGD1CacheConf.DEFAULT_SIZE},{CGD1CacheConf.DEFAULT_ASSOC},{CGD1CacheConf.DEFAULT_LINE_SIZE}'
    DEFAULT_LL_CONF = f'{CGLLCacheConf.DEFAULT_SIZE},{CGLLCacheConf.DEFAULT_ASSOC},{CGLLCacheConf.DEFAULT_LINE_SIZE}'
    prefix = config.OUT_PREFIX + r'\.' + config.PROGRAM_ALIAS + r'\.'
    cache = {}

    def __init__(self):
        self.REGEXES = {
            'D1': {
                'size': self.prefix + r'[0-9]+,' + str(CGD1CacheConf.DEFAULT_ASSOC) + r','
                        + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF,
                'assoc': self.prefix + str(CGD1CacheConf.DEFAULT_SIZE) + r',[0-9]+,'
                         + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF,
                'line_size': self.prefix + str(CGD1CacheConf.DEFAULT_SIZE) + r','
                             + str(CGD1CacheConf.DEFAULT_ASSOC) + r',[0-9]+\.' + self.DEFAULT_LL_CONF
            },
            'LL': {
                'size': self.prefix + self.DEFAULT_D1_CONF + r'\.' + r'[0-9]+,'
                        + str(CGLLCacheConf.DEFAULT_ASSOC) + r',' + str(CGLLCacheConf.DEFAULT_LINE_SIZE),
                'assoc': self.prefix + self.DEFAULT_D1_CONF + r'\.' + str(CGLLCacheConf.DEFAULT_SIZE)
                         + r',[0-9]+,' + str(CGLLCacheConf.DEFAULT_LINE_SIZE),
                'line_size': self.prefix + self.DEFAULT_D1_CONF + r'\.' + str(CGLLCacheConf.DEFAULT_SIZE)
                             + r',' + str(CGLLCacheConf.DEFAULT_ASSOC) + r',[0-9]+'
            }
        }

    def parse(self, key):
        if key not in self.cache:
            self.cache[key] = CGParser(f'{config.OUT_DIR}/{key}').parse()
            return self.cache[key]
        return self.cache[key]

    def get_for_param(self, cache, param):
        outputs = []

        for f in os.listdir(config.OUT_DIR):
            if re.match(self.REGEXES[cache][param], f):
                outputs.append(self.parse(f))

        return sorted(outputs, key=lambda o: int(o.get_specs()[cache][param]))

    def get_for_program(self):
        outputs = []
        for f in os.listdir(config.OUT_DIR):
            if re.match(self.prefix, f):
                outputs.append(self.parse(f))

        return outputs
