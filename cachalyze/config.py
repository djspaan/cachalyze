PROGRAM_ALIAS = 'test'
PROGRAM_CMD = '/home/dennisspaan/Workspace/test/bld/app/test -s -c \
              /home/dennisspaan/Workspace/test/bld/app/test.xml'
N_THREADS = 4
MAX_PLOTTED_FUNCS = 5

# ANALYZE
THRESHOLD = 99.9
INCLUDE_STANDARD_METHODS = False
INCLUDE_FOLDER = '/home/dennisspaan/Workspace/test/libs'
MIN_MISS_RATE = 0.5

CACHE_PARAMS = {
    'D1': {
        'SIZE': [8192, 16384, 32768, 65536, 131072, 262144],
        'ASSOC': [2, 4, 8, 16, 32, 64],
        'LINE_SIZE': [32, 64, 128, 256]
    },
    'LL': {
        'SIZE': [2097152, 4194304, 8388608, 16777216, 33554432, 67108864],
        'ASSOC': [2, 4, 8, 16, 32, 64],
        'LINE_SIZE': [32, 64, 128, 256]
    }
}

# STORAGE
SAVE_FIGURE = True
OUT_DIR = 'out'
OUT_PREFIX = 'cgrunner.out'

# CACHEGRIND RUN CONFIG
# PROGRAM_CMD = 'data/sample_programs/good_cacher'
# PROGRAM_CMD = 'timeout 5m /home/dennisspaan/Workspace/hub/build/local_subscriber/local_subscriber -s -c \
#                     /home/dennisspaan/Workspace/hub/conf/local_subscriber.xml'
# PROGRAM_CMD = '/home/dennisspaan/Workspace/test/bld/app/test -s -c \
#               /home/dennisspaan/Workspace/test/bld/app/test.xml'

