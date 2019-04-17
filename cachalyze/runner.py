import pickle
import asyncio
from math import ceil
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# from cachalyze.cganalyzer import CGAnalyzer
# from cachalyze.cgparser import CGParser
from cachalyze.cgrunner import CGRunner


def run():
    # RUN AND SAVE CG
    cg('D1', 'bad_cacher')

    # PLOT D1 STATISTICS
    # plot_d1('bad_cacher')

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


async def cg_run_size(program, cache_level, params=[]):
    params = [8192, 16384, 32768, 65536, 131072, 262144]  # ll sizes
    runs = [await CGRunner('data/sample_programs/' + program,
                           ['--{}={},16,64'.format(cache_level, str(param))]).run() for param in params]
    pickle.dump(runs, open('out/' + program + '-' + cache_level + '-size.bin', 'w+b'))


async def cg_run_assoc(program, cache_level, params=[]):
    params = [2, 4, 8, 16, 32, 64]  # n-ways set assoc
    runs = [await CGRunner('data/sample_programs/' + program,
                     ['--{}=8388608,{},64'.format(cache_level, str(param))]).run() for param in params]
    pickle.dump(runs, open('out/' + program + '-' + cache_level + '-assoc.bin', 'w+b'))


async def cg_run_line(program, cache_level, params=[]):
    params = [32, 64, 128, 256]  # ll line-sizes
    runs = [await CGRunner('data/sample_programs/' + program,
                     ['--{}=8388608,16,{}'.format(cache_level, str(param))]).run() for param in params]
    pickle.dump(runs, open('out/' + program + '-' + cache_level + '-line.bin', 'w+b'))


def cg(cache_level, program):
    import time
    loop = asyncio.get_event_loop()
    s = time.perf_counter()
    loop.run_until_complete(asyncio.wait([
        cg_run_size(program, cache_level), cg_run_assoc(program, cache_level), cg_run_line(program, cache_level)]))
    elapsed = time.perf_counter() - s
    print(f"executed in {elapsed:0.2f} seconds.")
    loop.close()


def plot_d1(program):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))

    # SIZE
    runs = pickle.load(open('out/' + program + '-D1-size.bin', 'rb'))
    sizes = [str(int(int(r.get_specs()['D1']['size']) / (1024))) + 'KB' for r in runs]
    miss_rates = [r.summary.D1mr / r.summary.Dr * 100 for r in runs]

    size_ax = axs[0]
    size_ax.plot(sizes, miss_rates, 's-r')
    size_ax.set_ylim([0, ceil(max(miss_rates))])
    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('data read miss rate')
    size_ax.set_title('size')
    size_ax.grid()

    # ASSOC
    runs = pickle.load(open('out/' + program + '-D1-assoc.bin', 'rb'))
    sizes = [r.get_specs()['D1']['assoc'] for r in runs]
    miss_rates = [r.summary.D1mr / r.summary.Dr * 100 for r in runs]

    assoc_ax = axs[1]
    assoc_ax.plot(sizes, miss_rates, 's-r')
    assoc_ax.set_ylim([0, ceil(max(miss_rates))])
    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    runs = pickle.load(open('out/' + program + '-D1-line.bin', 'rb'))
    sizes = [r.get_specs()['D1']['line_size'] + 'B' for r in runs]
    miss_rates = [r.summary.D1mr / r.summary.Dr * 100 for r in runs]

    line_ax = axs[2]
    line_ax.plot(sizes, miss_rates, 's-r')
    line_ax.set_ylim([0, ceil(max(miss_rates))])
    line_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    line_ax.set_title('line size')
    line_ax.grid()

    # plt.savefig(program + '_d1')
    plt.show()


def plot_ll(program):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))

    # SIZE
    runs = pickle.load(open('out/' + program + '-LL-size.bin', 'rb'))
    sizes = [str(int(int(r.get_specs()['LL']['size']) / (1024 * 1024))) + 'MB' for r in runs]
    miss_rates = [r.summary.DLmr / r.summary.Dr * 100 for r in runs]

    size_ax = axs[0]
    size_ax.plot(sizes, miss_rates, 's-r')
    size_ax.set_ylim([0, ceil(max(miss_rates))])
    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('data read miss rate')
    size_ax.set_title('size')
    size_ax.grid()

    # ASSOC
    runs = pickle.load(open('out/' + program + '-LL-assoc.bin', 'rb'))
    sizes = [r.get_specs()['LL']['assoc'] for r in runs]
    miss_rates = [r.summary.DLmr / r.summary.Dr * 100 for r in runs]

    assoc_ax = axs[1]
    assoc_ax.plot(sizes, miss_rates, 's-r')
    assoc_ax.set_ylim([0, ceil(max(miss_rates))])
    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    runs = pickle.load(open('out/' + program + '-LL-line.bin', 'rb'))
    sizes = [r.get_specs()['LL']['line_size'] + 'B' for r in runs]
    miss_rates = [r.summary.DLmr / r.summary.Dr * 100 for r in runs]

    line_ax = axs[2]
    line_ax.plot(sizes, miss_rates, 's-r')
    line_ax.set_ylim([0, ceil(max(miss_rates))])
    line_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    line_ax.set_title('line size')
    line_ax.grid()

    # plt.savefig(program + '_ll')
    plt.show()
