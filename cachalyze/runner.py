import asyncio
from math import ceil, floor
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from cachalyze.cganalyzer import CGAnalyzer, CGGlobalAnalyzer
from cachalyze.cgrunner import CGRunner, CGRunConf, CGD1CacheConf, CGLLCacheConf
from cachalyze.cgstorage import CGStorage

N_THREADS = 4
MAX_PLOTTED_FUNCS = 5


def run():
    pass

    # output = CGParser('out/cgrunner.out.local_subscriber.32768,8,64.8388608,16,64').parse()
    # analyse = CGAnalyzer(output)
    # for func in analyse.get_thresholded_functions():
    #     print('{} {}'.format(func.events, func))

    # runner = CGRunner(CGRunConf())
    # print(runner.run())

    # RUN AND SAVE CG
    # cg()

    # PLOT D1 STATISTICS
    # plot_app_d1('test', total_misses_d1)
    # plot_app_ll('test', total_misses_ll)
    plot_funcs_d1('test', total_misses_d1)
    # plot_funcs_ll('test', total_misses_ll)

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


def cg():
    confs = [
        *[CGRunConf(d1=CGD1CacheConf(size=i)) for i in [8192, 16384, 32768, 65536, 131072, 262144]],
        *[CGRunConf(d1=CGD1CacheConf(assoc=i)) for i in [2, 4, 8, 16, 32, 64]],
        *[CGRunConf(d1=CGD1CacheConf(line_size=i)) for i in [32, 64, 128, 256]],
        *[CGRunConf(ll=CGLLCacheConf(size=i)) for i in [2097152, 4194304, 8388608, 16777216, 33554432, 67108864]],
        *[CGRunConf(ll=CGLLCacheConf(assoc=i)) for i in [2, 4, 8, 16, 32, 64]],
        *[CGRunConf(ll=CGLLCacheConf(line_size=i)) for i in [32, 64, 128, 256]]
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait([cg_run_queue(loop, confs)]))
    loop.close()


def total_misses_d1(events):
    if events.Dr + events.Dw == 0:
        return 0
    return (events.D1mr + events.D1mw) / (events.Dr + events.Dw) * 100


def read_misses_d1(events):
    if events.Dr == 0:
        return 0
    return events.D1mr / events.Dr * 100


def write_misses_d1(events):
    if events.Dw == 0:
        return 0
    return events.D1mw / events.Dw * 100


def total_misses_ll(events):
    if events.Dr + events.Dw == 0:
        return 0
    return (events.DLmr + events.DLmw) / (events.Dr + events.Dw) * 100


def read_misses_ll(events):
    if events.Dr == 0:
        return 0
    return events.DLmr / events.Dr * 100


def write_misses_ll(events):
    if events.Dw == 0:
        return 0
    return events.DLmw / events.Dw * 100


def plot_funcs_d1(program, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    size_ax = axs[0]
    runs = CGStorage(program).get_for_param('D1', 'size')
    sizes = [str(int(int(r.get_specs()['D1']['size']) / 1024)) + 'KB' for r in runs]
    thresholded_funcs = CGGlobalAnalyzer(runs).get_functions_by_change()[:MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [count_func(f.events) for f in funcs]
        size_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('D1 r+w miss rate')
    size_ax.set_title('size')
    size_ax.legend()
    size_ax.grid()

    # ASSOC
    assoc_ax = axs[1]
    runs = CGStorage(program).get_for_param('D1', 'assoc')
    sizes = [r.get_specs()['D1']['assoc'] for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [count_func(f.events) for f in funcs]
        assoc_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    line_ax = axs[2]
    runs = CGStorage(program).get_for_param('D1', 'line_size')
    sizes = [r.get_specs()['D1']['line_size'] + 'B' for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [count_func(f.events) for f in funcs]
        line_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    line_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    line_ax.set_title('line size')
    line_ax.grid()

    min_miss_rate = floor(min(min_miss_rates))
    max_miss_rate = ceil(max(max_miss_rates))
    size_ax.set_ylim([min_miss_rate, max_miss_rate])
    assoc_ax.set_ylim([min_miss_rate, max_miss_rate])
    line_ax.set_ylim([min_miss_rate, max_miss_rate])

    plt.tight_layout()
    plt.savefig(program + '_funcs_d1')
    plt.show()


def plot_funcs_ll(program, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    size_ax = axs[0]
    runs = CGStorage(program).get_for_param('LL', 'size')
    sizes = [str(int(int(r.get_specs()['LL']['size']) / (1024 * 1024))) + 'MB' for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [count_func(f.events) for f in funcs]
        size_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('LL r+w miss rate')
    size_ax.set_title('size')
    size_ax.legend()
    size_ax.grid()

    # ASSOC
    assoc_ax = axs[1]
    runs = CGStorage(program).get_for_param('LL', 'assoc')
    sizes = [r.get_specs()['LL']['assoc'] for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [count_func(f.events) for f in funcs]
        assoc_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    line_ax = axs[2]
    runs = CGStorage(program).get_for_param('LL', 'line_size')
    sizes = [r.get_specs()['LL']['line_size'] + 'B' for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:MAX_PLOTTED_FUNCS]
    max_miss_rates = []
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [count_func(f.events) for f in funcs]
        line_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    line_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    line_ax.set_title('line size')
    line_ax.grid()

    min_miss_rate = floor(min(min_miss_rates))
    max_miss_rate = ceil(max(max_miss_rates))
    size_ax.set_ylim([min_miss_rate, max_miss_rate])
    assoc_ax.set_ylim([min_miss_rate, max_miss_rate])
    line_ax.set_ylim([min_miss_rate, max_miss_rate])

    plt.tight_layout()
    plt.savefig(program + '_funcs_ll')
    plt.show()


def plot_app_d1(program, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    runs = CGStorage(program).get_for_param('D1', 'size')
    sizes = [str(int(int(r.get_specs()['D1']['size']) / 1024)) + 'KB' for r in runs]
    miss_rates = [count_func(r.summary) for r in runs]
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    size_ax = axs[0]
    size_ax.plot(sizes, miss_rates, 's-r')
    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('D1 r+w miss rate')
    size_ax.set_title('size')
    size_ax.grid()

    # ASSOC
    runs = CGStorage(program).get_for_param('D1', 'assoc')
    sizes = [r.get_specs()['D1']['assoc'] for r in runs]
    miss_rates = [count_func(r.summary) for r in runs]
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    assoc_ax = axs[1]
    assoc_ax.plot(sizes, miss_rates, 's-r')
    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    runs = CGStorage(program).get_for_param('D1', 'line_size')
    sizes = [r.get_specs()['D1']['line_size'] + 'B' for r in runs]
    miss_rates = [count_func(r.summary) for r in runs]
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    line_ax = axs[2]
    line_ax.plot(sizes, miss_rates, 's-r')
    line_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    line_ax.set_title('line size')
    line_ax.grid()

    min_miss_rate = floor(min(min_miss_rates))
    max_miss_rate = ceil(max(max_miss_rates))
    size_ax.set_ylim([min_miss_rate, max_miss_rate])
    assoc_ax.set_ylim([min_miss_rate, max_miss_rate])
    line_ax.set_ylim([min_miss_rate, max_miss_rate])

    plt.tight_layout()
    plt.savefig(program + '_app_d1')
    plt.show()


def plot_app_ll(program, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    runs = CGStorage(program).get_for_param('LL', 'size')
    sizes = [str(int(int(r.get_specs()['LL']['size']) / (1024 * 1024))) + 'MB' for r in runs]
    miss_rates = [count_func(r.summary) for r in runs]
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    size_ax = axs[0]
    size_ax.plot(sizes, miss_rates, 's-r')
    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('LL r+w miss rate')
    size_ax.set_title('size')
    size_ax.grid()

    # ASSOC
    runs = CGStorage(program).get_for_param('LL', 'assoc')
    sizes = [r.get_specs()['LL']['assoc'] for r in runs]
    miss_rates = [count_func(r.summary) for r in runs]
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    assoc_ax = axs[1]
    assoc_ax.plot(sizes, miss_rates, 's-r')
    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    runs = CGStorage(program).get_for_param('LL', 'line_size')
    sizes = [r.get_specs()['LL']['line_size'] + 'B' for r in runs]
    miss_rates = [count_func(r.summary) for r in runs]
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    line_ax = axs[2]
    line_ax.plot(sizes, miss_rates, 's-r')
    line_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    line_ax.set_title('line size')
    line_ax.grid()

    min_miss_rate = floor(min(min_miss_rates))
    max_miss_rate = ceil(max(max_miss_rates))
    size_ax.set_ylim([min_miss_rate, max_miss_rate])
    assoc_ax.set_ylim([min_miss_rate, max_miss_rate])
    line_ax.set_ylim([min_miss_rate, max_miss_rate])

    plt.tight_layout()
    plt.savefig(program + '_app_ll')
    plt.show()


def plot_test(program, count_func):
    # fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    fig, axs = plt.subplots(figsize=(80, 80))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    # size_ax = axs[0]
    size_ax = axs
    runs = CGStorage(program).get_for_param('D1', 'size')
    sizes = [str(int(int(r.get_specs()['D1']['size']) / 1024)) + 'KB' for r in runs]
    thresholded_funcs = CGGlobalAnalyzer(runs).get_functions_by_change()[:MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
        miss_rates = [count_func(f.events) for f in funcs]
        size_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('D1 r+w miss rate')
    size_ax.set_title('size')
    size_ax.legend()
    size_ax.grid()

    # ASSOC
    # assoc_ax = axs[1]
    # runs = CGStorage(program).get_for_param('D1', 'assoc')
    # sizes = [r.get_specs()['D1']['assoc'] for r in runs]
    # thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:MAX_PLOTTED_FUNCS]
    # for func in thresholded_funcs:
    #     funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
    #     miss_rates = [count_func(f.events) for f in funcs]
    #     assoc_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
    #     min_miss_rates.append(min(miss_rates))
    #     max_miss_rates.append(max(miss_rates))
    #
    # assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    # assoc_ax.set_title('set-associativity')
    # assoc_ax.grid()

    # LINE
    # line_ax = axs[2]
    # runs = CGStorage(program).get_for_param('D1', 'line_size')
    # sizes = [r.get_specs()['D1']['line_size'] + 'B' for r in runs]
    # thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:MAX_PLOTTED_FUNCS]
    # for func in thresholded_funcs:
    #     funcs = [f for r in runs for f in r.get_functions() if f.__str__() == func.__str__()]
    #     miss_rates = [count_func(f.events) for f in funcs]
    #     line_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
    #     min_miss_rates.append(min(miss_rates))
    #     max_miss_rates.append(max(miss_rates))
    #
    # line_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    # line_ax.set_title('line size')
    # line_ax.grid()

    min_miss_rate = floor(min(min_miss_rates))
    max_miss_rate = ceil(max(max_miss_rates))
    size_ax.set_ylim([min_miss_rate, max_miss_rate])
    # assoc_ax.set_ylim([min_miss_rate, max_miss_rate])
    # line_ax.set_ylim([min_miss_rate, max_miss_rate])

    plt.tight_layout()
    plt.savefig(program + '_test_d1')
    plt.show()