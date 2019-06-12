class Config:
    VERBOSE = False

    # RUN SIM
    PROGRAM_ALIAS = None
    PROGRAM_CMD = None
    N_THREADS = 2
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

    # ANALYZE
    REGION_THRESHOLD = 99.9
    LINE_THRESHOLD = 99.9
    INCLUDE_STANDARD_METHODS = False
    INCLUDE_DIR = ''

    # STORAGE
    SAVE_FIGURE = True
    OUT_DIR = ''
    OUT_PREFIX = 'callgrind.out'
