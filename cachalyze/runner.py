import pickle
import matplotlib.pyplot as plt

# from cachalyze.cganalyzer import CGAnalyzer
# from cachalyze.cgparser import CGParser
from cachalyze.cgrunner import CGRunner


def run():
    # # RUN MULTIPLE TIMES AND SAVE
    # sizes = [2097152, 4194304, 8388608, 16777216, 33554432, 67108864] # ll sizes
    # runs = [CGRunner('data/sample_programs/bad_cacher', ['--LL=' + str(size) + ',16,64']).run() for size in sizes]
    # pickle.dump(runs, open('out/cache.bin', 'wb'))
    # stats = [r.summary for r in runs]
    # for stat in stats:
    #     print(stat)

    # RETRIEVE SAVE
    runs = pickle.load(open('out/cache.bin', 'rb'))
    sizes = [str(int(int(r.get_specs()['LL']['size']) / (1024 * 1024))) + 'MB' for r in runs]
    lld_misses = [r.summary.DLmr / r.summary.Dr * 100 for r in runs]

    # PLOT
    plt.plot(sizes, lld_misses, 's-r')
    plt.grid()
    plt.show()

    # THRESHOLDED FUNCTIONS
    # analyzer = CGAnalyzer(output)
    # funcs = analyzer.get_thresholded_functions()
    # file = funcs[0].file
    # for func in output.get_functions():
    #     print('{} {}'.format(func.events, func))

    # PRINT LINES WITH EVENTS
    # print(file.path)
    # for event in output.events:
    #     print('{:>11}'.format(event), end='')
    # print('')
    # for line, content, events in file.get_lines_with_events():
    #     print('{} {}'.format(events.format(), content))
