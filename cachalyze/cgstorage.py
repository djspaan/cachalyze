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

    def parse(self, key):
        if key not in self.cache:
            self.cache[key] = CGParser(f'{config.OUT_DIR}/{key}').parse()
            return self.cache[key]
        return self.cache[key]

    def get_regex(self, cache, param):
        params = config.CACHE_PARAMS[cache][param]
        param_regex = "(" + "|".join(str(p) for p in params) + ")"
        regexes = {
            'D1': {
                'SIZE': self.prefix + param_regex + ',' + str(CGD1CacheConf.DEFAULT_ASSOC) + ','
                        + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF,
                'ASSOC': self.prefix + str(CGD1CacheConf.DEFAULT_SIZE) + ',' + param_regex + ','
                         + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF,
                'LINE_SIZE': self.prefix + str(CGD1CacheConf.DEFAULT_SIZE) + ','
                             + str(CGD1CacheConf.DEFAULT_ASSOC) + ',' + param_regex + r'\.'+ self.DEFAULT_LL_CONF
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

    def get_for_param(self, cache, param):
        outputs = []
        regex = self.get_regex(cache, param)

        for f in os.listdir(config.OUT_DIR):
            if re.match(regex, f):
                outputs.append(self.parse(f))

        return sorted(outputs, key=lambda o: int(o.get_specs()[cache][param]))

    def get_for_program(self):
        outputs = []
        for f in os.listdir(config.OUT_DIR):
            if re.match(self.prefix, f):
                outputs.append(self.parse(f))

        return outputs
