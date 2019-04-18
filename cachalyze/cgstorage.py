import glob

from cachalyze.cgrunner import CGD1CacheConf, CGLLCacheConf

# WIP
class CGStorage:
    OUT_DIR = 'out'
    PREFIX = 'cgrunner.out'

    def get_all(self):
        return glob.glob(f'{self.OUT_DIR}/*')

    def get_all_for_program(self, program):
        return glob.glob(f'{self.OUT_DIR}/{self.PREFIX}.{program}*')

    def get_for_param(self, program, cache, param):
        if cache == 'D1':
            pass

    def get_for_d1_size(self, program):
        # TODO: GLOB DOESNT DO REGEX FULLY
        return glob.glob(f'{self.OUT_DIR}/{self.PREFIX}.{program}.[0-9]+.{CGD1CacheConf.DEFAULT_ASSOC}*')
