from math import ceil, floor
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import cachalyze.config as config
from cachalyze.cganalyzer import CGGlobalAnalyzer, CGAnalyzer
from cachalyze.cgstorage import CGStorage


class CGSingleFuncSizeSubplot:
    def __init__(self, plot, axs, cache):
        self.parent_plot = plot
        self.axs = axs
        self.cache = cache

    def plot(self):
        runs = CGStorage(config.PROGRAM_ALIAS).get_for_param(self.cache, 'size')
        print(runs)
        # TODO: FIX SIZES HERE FOR CACHE
        sizes = [CGPlotter.convert_to_bit_str(s) for s in config.CACHE_PARAMS[self.cache]['SIZES']]
        print(str(self.parent_plot.func))
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(self.parent_plot.func)]
        print(len(runs))
        print(len(sizes))
        print(funcs)
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        print(miss_rates)
        quit()
        self.axs.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.parent_plot.min_miss_rates.append(min(miss_rates))
        self.parent_plot.max_miss_rates.append(max(miss_rates))
        self.axs.yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs.set_title('size')
        self.axs.legend()
        self.axs.grid()


class CGSingleFuncAssocSubplot:
    def __init__(self, plot, axs, cache):
        self.parent_plot = plot
        self.axs = axs
        self.cache = cache

    def plot(self):
        runs = CGStorage(config.PROGRAM_ALIAS).get_for_param(self.cache, 'assoc')
        sizes = [r.get_specs()[self.cache]['assoc'] for r in runs]
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(self.parent_plot.func)]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        self.axs.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.parent_plot.min_miss_rates.append(min(miss_rates))
        self.parent_plot.max_miss_rates.append(max(miss_rates))
        self.axs.yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs.set_title('set-associativity')
        self.axs.grid()


class CGSingleFuncLineSizeSubplot:
    def __init__(self, plot, axs, cache):
        self.parent_plot = plot
        self.axs = axs
        self.cache = cache

    def plot(self):
        runs = CGStorage(config.PROGRAM_ALIAS).get_for_param(self.cache, 'line_size')
        sizes = [r.get_specs()[self.cache]['line_size'] + 'B' for r in runs]
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(self.parent_plot.func)]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        self.axs.plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.parent_plot.min_miss_rates.append(min(miss_rates))
        self.parent_plot.max_miss_rates.append(max(miss_rates))
        self.axs.yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs.set_title('line size')
        self.axs.grid()


class CGPlot:
    def __init__(self, cache):
        self.cache = cache
        self.min_miss_rates = self.max_miss_rates = []
        self.fig, self.axs = plt.subplots(1, 3, figsize=(12, 3))

    def plot(self):
        self.plot_subplots()
        plt.tight_layout()
        # plt.savefig(program + '_funcs_d1')
        plt.show()

    def plot_subplots(self):
        raise Exception('CGPlot class is not instantiatable.')


class CGSingleFuncPlot(CGPlot):
    def __init__(self, cache, func):
        self.func = func
        super().__init__(cache)

    def plot_subplots(self):
        CGSingleFuncSizeSubplot(self, self.axs[0], self.cache).plot()
        CGSingleFuncAssocSubplot(self, self.axs[1], self.cache).plot()
        CGSingleFuncLineSizeSubplot(self, self.axs[2], self.cache).plot()
        min_miss_rate = floor(min(self.min_miss_rates))
        max_miss_rate = ceil(max(self.max_miss_rates))
        self.axs[0].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[1].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[2].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[0].set_ylabel(f'{self.cache} r+w miss rate')


class CGMultiFuncPlot:
    def plot(self):
        pass


class CGGlobalPlot:
    def plot(self):
        pass


class CGPlotter:
    @staticmethod
    def convert_to_bit_str(num_bits):
        if num_bits < 1024:
            return str(int(num_bits / 1024)) + 'KB'
        return str(int(num_bits / (1024 * 1024))) + 'MB'

    @staticmethod
    def plot_single_func(cache, func):
        CGSingleFuncPlot(cache, func).plot()

    def plot_func_d1(self, func, count_func):
        fig, axs = plt.subplots(1, 3, figsize=(12, 3))
        min_miss_rates = max_miss_rates = []

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

    def plot_func_ll(self, func, count_func):
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

    def plot_app_d1(self, count_func):
        fig, axs = plt.subplots(1, 3, figsize=(12, 3))
        min_miss_rates = max_miss_rates = []

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
        plt.savefig('out/' + config.PROGRAM_ALIAS + '_app_d1')
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
