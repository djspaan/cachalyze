import pickle
import asyncio
from math import ceil
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from cachalyze.cganalyzer import CGAnalyzer
# from cachalyze.cgparser import CGParser
from cachalyze.cgrunner import CGRunner, CGRunConf, CGD1CacheConf, CGLLCacheConf
from cachalyze.cgstorage import CGStorage

N_THREADS = 4


def run():
    pass

    print(CGStorage().get_for_d1_size('good_cacher'))

    # RUN AND SAVE CG
    # cg('good_cacher')

    # PLOT D1 STATISTICS
    # plot_app_d1('bad_cacher')
    # plot_funcs_d1('bad_cacher')

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


async def cg_run_conf(conf):
    await CGRunner(conf).run_async()


async def cg_run_queue(loop, confs):
    tasks = set()
    i = 0
    while i < len(confs):
        if len(tasks) >= N_THREADS:
            _done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        tasks.add(loop.create_task(cg_run_conf(confs[i])))
        i += 1
    await asyncio.wait(tasks)


def cg(program):
    confs = [
        *[CGRunConf(program, d1=CGD1CacheConf(size=i)) for i in [8192, 16384, 32768, 65536, 131072, 262144]],
        *[CGRunConf(program, d1=CGD1CacheConf(assoc=i)) for i in [2, 4, 8, 16, 32, 64]],
        *[CGRunConf(program, d1=CGD1CacheConf(line_size=i)) for i in [32, 64, 128, 256]],
        *[CGRunConf(program, ll=CGLLCacheConf(size=i)) for i in [2097152, 4194304, 8388608, 16777216, 33554432, 67108864]],
        *[CGRunConf(program, ll=CGLLCacheConf(assoc=i)) for i in [2, 4, 8, 16, 32, 64]],
        *[CGRunConf(program, ll=CGLLCacheConf(line_size=i)) for i in [32, 64, 128, 256]]
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait([cg_run_queue(loop, confs)]))
    loop.close()


def plot_funcs_d1(program):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))

    # SIZE
    size_ax = axs[0]
    runs = pickle.load(open('out/' + program + '-D1-size.bin', 'rb'))
    sizes = [str(int(int(r.get_specs()['D1']['size']) / 1024)) + 'KB' for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()
    # for f in runs[0].files:
    #     print(f.path)
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [f.events.D1mr / f.events.Dr * 100 for f in funcs]
        size_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        if ceil(max(miss_rates)) != 0:
            size_ax.set_ylim([0, ceil(max(miss_rates))])

    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('data read miss rate')
    size_ax.set_title('size')
    size_ax.legend()
    size_ax.grid()

    # ASSOC
    assoc_ax = axs[1]
    runs = pickle.load(open('out/' + program + '-D1-assoc.bin', 'rb'))
    sizes = [r.get_specs()['D1']['assoc'] for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [f.events.D1mr / f.events.Dr * 100 for f in funcs]
        assoc_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        if ceil(max(miss_rates)) != 0:
            assoc_ax.set_ylim([0, ceil(max(miss_rates))])

    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.legend()
    assoc_ax.grid()

    # LINE
    line_ax = axs[2]
    runs = pickle.load(open('out/' + program + '-D1-line.bin', 'rb'))
    sizes = [r.get_specs()['D1']['line_size'] + 'B' for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [f.events.D1mr / f.events.Dr * 100 for f in funcs]
        line_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        if ceil(max(miss_rates)) != 0:
            line_ax.set_ylim([0, ceil(max(miss_rates))])

    line_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    line_ax.set_title('line size')
    line_ax.legend()
    line_ax.grid()

    # plt.savefig(program + '_app_d1')
    plt.show()


def plot_app_d1(program):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))

    # SIZE
    runs = pickle.load(open('out/' + program + '-D1-size.bin', 'rb'))
    sizes = [str(int(int(r.get_specs()['D1']['size']) / 1024)) + 'KB' for r in runs]
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

    # plt.savefig(program + '_app_d1')
    plt.show()


def plot_app_ll(program):
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

    # plt.savefig(program + '_app_ll')
    plt.show()
