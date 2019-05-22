from math import ceil, floor
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import cachalyze.config as config
from cachalyze.cganalyzer import CGAnalyzer, CGGlobalAnalyzer
from cachalyze.cgstorage import CGStorage


def run():
    pass

    # SINGLE RUN WITH DEFAULT CONFIG
    # runner = CGRunner(CGRunConf())
    # print(runner.run())

    # RUN AND SAVE CG OUTPUT
    # CGAsyncRunner.run()

    # PLOT STATISTICS
    # plot_func_d1('test',
    #              '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h:Optiver::Common::Internal::Logger::Get()',
    #              CGAnalyzer.total_misses_d1)
    # plot_func_ll('test',
    #              '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h:Optiver::Common::Internal::Logger::Get()',
    #              CGAnalyzer.total_misses_ll)
    # plot_app_d1('ls', CGAnalyzer.total_misses_d1)
    # plot_app_ll('ls', CGAnalyzer.total_misses_ll)
    # plot_funcs_d1('test', CGAnalyzer.total_misses_d1)
    # plot_funcs_ll('test', CGAnalyzer.total_misses_ll)

    # PRINT THRESHOLDED FUNCTIONS
    # output = CGParser('out/cgrunner.out.local_subscriber.32768,8,64.8388608,16,64').parse()
    # analyse = CGAnalyzer(output)
    # for func in analyse.get_thresholded_functions():
    #     print('{} {}'.format(func.events, func))

    # PRINT LINES WITH EVENTS
    # print(file.path)
    # for event in output.events:
    #     print('{:>11}'.format(event), end='')
    # print('')
    # for line, content, events in file.get_lines_with_events():
    #     print('{} {}'.format(events.format(), content))


def plot_func_d1(program, func, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    size_ax = axs[0]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'size')
    sizes = [str(int(int(r.get_specs()['D1']['size']) / 1024)) + 'KB' for r in runs]
    funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
    miss_rates = [count_func(f.events) for f in funcs]
    size_ax.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('D1 r+w miss rate')
    size_ax.set_title('size')
    size_ax.legend()
    size_ax.grid()

    # ASSOC
    assoc_ax = axs[1]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'assoc')
    sizes = [r.get_specs()['D1']['assoc'] for r in runs]
    funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
    miss_rates = [count_func(f.events) for f in funcs]
    assoc_ax.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    line_ax = axs[2]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'line_size')
    sizes = [r.get_specs()['D1']['line_size'] + 'B' for r in runs]
    funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
    miss_rates = [count_func(f.events) for f in funcs]
    line_ax.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
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
    # plt.savefig(program + '_funcs_d1')
    plt.show()


def plot_func_ll(program, func, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    size_ax = axs[0]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'size')
    sizes = [str(int(int(r.get_specs()['LL']['size']) / (1024 * 1024))) + 'MB' for r in runs]
    funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
    miss_rates = [count_func(f.events) for f in funcs]
    size_ax.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    size_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    size_ax.set_ylabel('LL r+w miss rate')
    size_ax.set_title('size')
    size_ax.legend()
    size_ax.grid()

    # ASSOC
    assoc_ax = axs[1]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'assoc')
    sizes = [r.get_specs()['LL']['assoc'] for r in runs]
    funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
    miss_rates = [count_func(f.events) for f in funcs]
    assoc_ax.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
    min_miss_rates.append(min(miss_rates))
    max_miss_rates.append(max(miss_rates))

    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    line_ax = axs[2]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'line_size')
    sizes = [r.get_specs()['LL']['line_size'] + 'B' for r in runs]
    funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
    miss_rates = [count_func(f.events) for f in funcs]
    line_ax.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
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
    # plt.savefig('out/' + program + '_func_ll')
    plt.show()


def plot_funcs_d1(program, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    size_ax = axs[0]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'size')
    sizes = [str(int(int(r.get_specs()['D1']['size']) / 1024)) + 'KB' for r in runs]
    thresholded_funcs = CGGlobalAnalyzer(runs).get_functions_by_change()[:config.MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
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
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'assoc')
    sizes = [r.get_specs()['D1']['assoc'] for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:config.MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
        miss_rates = [count_func(f.events) for f in funcs]
        assoc_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    line_ax = axs[2]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'line_size')
    sizes = [r.get_specs()['D1']['line_size'] + 'B' for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:config.MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
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
    plt.savefig('out/' + program + '_funcs_d1')
    plt.show()


def plot_funcs_ll(program, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    size_ax = axs[0]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'size')
    sizes = [str(int(int(r.get_specs()['LL']['size']) / (1024 * 1024))) + 'MB' for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:config.MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
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
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'assoc')
    sizes = [r.get_specs()['LL']['assoc'] for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:config.MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
        miss_rates = [count_func(f.events) for f in funcs]
        assoc_ax.plot(sizes, miss_rates, 's-', label=func.get_formatted_name())
        min_miss_rates.append(min(miss_rates))
        max_miss_rates.append(max(miss_rates))

    assoc_ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    assoc_ax.set_title('set-associativity')
    assoc_ax.grid()

    # LINE
    line_ax = axs[2]
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'line_size')
    sizes = [r.get_specs()['LL']['line_size'] + 'B' for r in runs]
    thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:config.MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
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
    plt.savefig('out/' + program + '_funcs_ll')
    plt.show()


def plot_app_d1(program, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'size')
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
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'assoc')
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
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'line_size')
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
    plt.savefig('out/' + program + '_app_d1')
    plt.show()


def plot_app_ll(program, count_func):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'size')
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
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'assoc')
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
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('LL', 'line_size')
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
    plt.savefig('out/' + program + '_app_ll')
    plt.show()


def plot_test(program, count_func):
    # fig, axs = plt.subplots(1, 3, figsize=(12, 3))
    fig, axs = plt.subplots(figsize=(80, 80))
    min_miss_rates = []
    max_miss_rates = []

    # SIZE
    # size_ax = axs[0]
    size_ax = axs
    runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'size')
    sizes = [str(int(int(r.get_specs()['D1']['size']) / 1024)) + 'KB' for r in runs]
    thresholded_funcs = CGGlobalAnalyzer(runs).get_functions_by_change()[:config.MAX_PLOTTED_FUNCS]
    for func in thresholded_funcs:
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
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
    # runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'assoc')
    # sizes = [r.get_specs()['D1']['assoc'] for r in runs]
    # thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:config.MAX_PLOTTED_FUNCS]
    # for func in thresholded_funcs:
    #     funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
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
    # runs = CGStorage(config.PROGRAM_ALIAS).get_for_param('D1', 'line_size')
    # sizes = [r.get_specs()['D1']['line_size'] + 'B' for r in runs]
    # thresholded_funcs = CGAnalyzer(runs[0]).get_thresholded_functions()[:config.MAX_PLOTTED_FUNCS]
    # for func in thresholded_funcs:
    #     funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
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
    plt.savefig('out/' + program + '_test_d1')
    plt.show()
