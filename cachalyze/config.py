PROGRAM_ALIAS = 'ls'
PROGRAM_CMD = 'ls -a'
N_THREADS = 4
MAX_PLOTTED_FUNCS = 5

D1_CACHE_SIZES = [8192, 16384, 32768, 65536, 131072, 262144]
D1_CACHE_ASSOCS = [2, 4, 8, 16, 32, 64]
D1_CACHE_LINE_SIZES = [32, 64, 128, 256]
LL_CACHE_SIZES = [2097152, 4194304, 8388608, 16777216, 33554432, 67108864]
LL_CACHE_ASSOCS = [2, 4, 8, 16, 32, 64]
LL_CACHE_LINE_SIZES = [32, 64, 128, 256]


# CACHEGRIND RUN CONFIG
# PROGRAM_CMD = 'data/sample_programs/bad_cacher'
# PROGRAM_CMD = 'timeout 5m /home/dennisspaan/Workspace/hub/build/local_subscriber/local_subscriber -s -c \
#                     /home/dennisspaan/Workspace/hub/conf/local_subscriber.xml'
# PROGRAM_CMD = '/home/dennisspaan/Workspace/test/bld/app/test -s -c \
#               /home/dennisspaan/Workspace/test/bld/app/test.xml'




