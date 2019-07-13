import os
import re
import pickle

from cachalyze.config import Config
from cachalyze.cgparser import CGParser
from cachalyze.cgrunners import CGD1CacheConf, CGLLCacheConf
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
        self.prefix = re.escape(Config.OUT_PREFIX) + r'\.' + re.escape(Config.PROGRAM_ALIAS) + r'\.' #

    def get(self, file):
        if file not in self._cache:
            pklfile = f'{Config.OUT_DIR}/{file}.pkl'
            if os.path.exists(pklfile):
                infile = open(pklfile, 'rb')
                self._cache[file] = pickle.load(infile)
                infile.close()
                Logger.info(f'Found already parsed output file binary: {Config.OUT_DIR}/{file}')
            else:
                self._cache[file] = CGParser(f'{Config.OUT_DIR}/{file}').parse()
                outfile = open(pklfile, 'wb')
                pickle.dump(self._cache[file], outfile)
                outfile.close()
                Logger.info(f'Successfully parsed output file: {Config.OUT_DIR}/{file}')
        return self._cache[file]

    def get_regex(self, cache, param):
        params = Config.CACHE_PARAMS[cache][param]
        param_regex = "(" + "|".join(str(p) for p in params) + ")"
        regexes = {
            'D1': {
                'SIZE': self.prefix + param_regex + ',' + str(CGD1CacheConf.DEFAULT_ASSOC) + ','
                        + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF  + r'\.' + re.escape(Config.OUT_EXT) + r'$',
                'ASSOC': self.prefix + str(CGD1CacheConf.DEFAULT_SIZE) + ',' + param_regex + ','
                         + str(CGD1CacheConf.DEFAULT_LINE_SIZE) + r'\.' + self.DEFAULT_LL_CONF  + r'\.' + re.escape(Config.OUT_EXT) + r'$',
                'LINE_SIZE': self.prefix + str(CGD1CacheConf.DEFAULT_SIZE) + ','
                             + str(CGD1CacheConf.DEFAULT_ASSOC) + ',' + param_regex + r'\.' + self.DEFAULT_LL_CONF  + r'\.' + re.escape(Config.OUT_EXT) + r'$',
            },
            'LL': {
                'SIZE': self.prefix + self.DEFAULT_D1_CONF + r'\.' + param_regex + ','
                        + str(CGLLCacheConf.DEFAULT_ASSOC) + r',' + str(CGLLCacheConf.DEFAULT_LINE_SIZE)  + r'\.' + re.escape(Config.OUT_EXT) + r'$',
                'ASSOC': self.prefix + self.DEFAULT_D1_CONF + r'\.' + str(CGLLCacheConf.DEFAULT_SIZE)
                         + ',' + param_regex + ',' + str(CGLLCacheConf.DEFAULT_LINE_SIZE)  + r'\.' + re.escape(Config.OUT_EXT) + r'$',
                'LINE_SIZE': self.prefix + self.DEFAULT_D1_CONF + r'\.' + str(CGLLCacheConf.DEFAULT_SIZE)
                             + r',' + str(CGLLCacheConf.DEFAULT_ASSOC) + ',' + param_regex  + r'\.' + re.escape(Config.OUT_EXT) + r'$'
            }
        }
        return regexes[cache][param]

    def get_for_run_conf(self, rc):
        regex = self.prefix + str(rc.d1.size) + ',' + str(rc.d1.assoc) + ',' + str(rc.d1.line_size) + r'\.' \
                + str(rc.ll.size) + ',' + str(rc.ll.assoc) + ',' + str(rc.ll.line_size) + r'\.' + re.escape(Config.OUT_EXT) + r'$'

        for f in os.listdir(Config.OUT_DIR):
            if re.match(regex, f):
                return self.get(f)

    def get_for_param(self, cache, param):
        outputs = []
        regex = self.get_regex(cache, param)

        for f in os.listdir(Config.OUT_DIR):
            if re.match(regex, f):
                outputs.append(self.get(f))

        return sorted(outputs, key=lambda o: int(o.get_specs()[cache][param]))

    def get_for_program(self):
        outputs = []
        for f in os.listdir(Config.OUT_DIR):
            if re.match(self.prefix + r'[\d,]+\.[\d,]+\.' + re.escape(Config.OUT_EXT) + r'$', f):
                outputs.append(self.get(f))

        if not len(outputs):
            Logger.error('No output files found. Make sure that the --out-folder and --out-prefix options are '
                         'correctly set')

        return outputs
