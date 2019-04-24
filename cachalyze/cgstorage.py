import os
import re

from cachalyze.cgparser import CGParser
from cachalyze.cgrunner import CGD1CacheConf, CGLLCacheConf


class CGStorage:
    OUT_DIR = 'out'
    PREFIX = 'cgrunner.out'
    DEFAULT_D1_CONF = f'{CGD1CacheConf.DEFAULT_SIZE},{CGD1CacheConf.DEFAULT_ASSOC},{CGD1CacheConf.DEFAULT_LINE_SIZE}'
    DEFAULT_LL_CONF = f'{CGLLCacheConf.DEFAULT_SIZE},{CGLLCacheConf.DEFAULT_ASSOC},{CGLLCacheConf.DEFAULT_LINE_SIZE}'
    REGEXES = ''

    def __init__(self, program):
        prefix = self.PREFIX + r'\.' + program + r'\.'
        self.REGEXES = {
            'D1': {
                'size': prefix + r'[0-9]+,' + str(CGD1CacheConf.DEFAULT_ASSOC) + r','
                + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF,
                'assoc': prefix + str(CGD1CacheConf.DEFAULT_SIZE) + r',[0-9]+,'
                + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF,
                'line_size': prefix + str(CGD1CacheConf.DEFAULT_SIZE) + r','
                + str(CGD1CacheConf.DEFAULT_ASSOC) + r',[0-9]+\.' + self.DEFAULT_LL_CONF
            },
            'LL': {
                'size': prefix + self.DEFAULT_D1_CONF + r'\.' + r'[0-9]+,'
                + str(CGLLCacheConf.DEFAULT_ASSOC) + r',' + str(CGLLCacheConf.DEFAULT_LINE_SIZE),
                'assoc': prefix + self.DEFAULT_D1_CONF + r'\.' + str(CGLLCacheConf.DEFAULT_SIZE)
                + r',[0-9]+,' + str(CGLLCacheConf.DEFAULT_LINE_SIZE),
                'line_size': prefix + self.DEFAULT_D1_CONF + r'\.' + str(CGLLCacheConf.DEFAULT_SIZE)
                + r',' + str(CGLLCacheConf.DEFAULT_ASSOC) + r',[0-9]+'
            }
        }

    def get_for_param(self, cache, param):
        outputs = [CGParser(f'{self.OUT_DIR}/{f}').parse() for f in os.listdir(self.OUT_DIR)
                   if re.match(self.REGEXES[cache][param], f)]
        return sorted(outputs, key=lambda o: int(o.get_specs()[cache][param]))
