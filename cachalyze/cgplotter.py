from math import ceil, floor
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import cachalyze.config as config
from cachalyze.cganalyzer import CGGlobalAnalyzer, CGAnalyzer
from cachalyze.cgstorage import CGStorage


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
        # SIZE
        runs = CGStorage().get_for_param(self.cache, 'size')
        sizes = [CGPlotter.convert_to_bit_str(s) for s in config.CACHE_PARAMS[self.cache]['SIZES']]
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(self.func)]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        self.axs[0].plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))
        self.axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[0].set_title('size')

        self.axs[0].grid()

        # ASSOC
        runs = CGStorage().get_for_param(self.cache, 'assoc')
        sizes = [r.get_specs()[self.cache]['assoc'] for r in runs]
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(self.func)]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        self.axs[1].plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))
        self.axs[1].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[1].set_title('set-associativity')
        self.axs[1].grid()

        # LINE SIZE
        runs = CGStorage().get_for_param(self.cache, 'line_size')
        sizes = [r.get_specs()[self.cache]['line_size'] + 'B' for r in runs]
        funcs = [f for r in runs for f in r.get_functions() if str(f) == str(self.func)]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        self.axs[2].plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))
        self.axs[2].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[2].set_title('line size')
        self.axs[2].grid()
        self.axs[2].legend()

        min_miss_rate = floor(min(self.min_miss_rates))
        max_miss_rate = ceil(max(self.max_miss_rates))

        self.axs[0].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[1].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[2].set_ylim([min_miss_rate, max_miss_rate])

        self.axs[0].set_ylabel(f'{self.cache} r+w miss rate')


class CGMultiFuncPlot(CGPlot):
    def __init__(self, cache, funcs):
        self.funcs = funcs
        super().__init__(cache)

    def plot_subplots(self):
        # SIZE
        runs = CGStorage().get_for_param(self.cache, 'size')
        sizes = [CGPlotter.convert_to_bit_str(s) for s in config.CACHE_PARAMS[self.cache]['SIZES']]
        for func in self.funcs:
            funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
            self.axs[0].plot(sizes, miss_rates, 's-', label=str(funcs[0]))
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[0].set_title('size')
        self.axs[0].grid()
        self.axs[0].legend()

        for l in self.axs[0].get_lines():
            print(f'{l.get_color()} - {l.get_label()}')

        # ASSOC
        runs = CGStorage().get_for_param(self.cache, 'assoc')
        sizes = [r.get_specs()[self.cache]['assoc'] for r in runs]
        for func in self.funcs:
            funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
            self.axs[1].plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[1].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[1].set_title('set-associativity')
        self.axs[1].grid()

        # LINE
        runs = CGStorage().get_for_param(self.cache, 'line_size')
        sizes = [r.get_specs()[self.cache]['line_size'] + 'B' for r in runs]
        for func in self.funcs:
            funcs = [f for r in runs for f in r.get_functions() if str(f) == str(func)]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
            self.axs[2].plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[2].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[2].set_title('line size')
        self.axs[2].grid()

        min_miss_rate = floor(min(self.min_miss_rates))
        max_miss_rate = ceil(max(self.max_miss_rates))
        self.axs[0].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[1].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[2].set_ylim([min_miss_rate, max_miss_rate])

        self.axs[0].set_ylabel(f'{self.cache} r+w miss rate')


class CGGlobalPlot(CGPlot):
    def plot_subplots(self):
        # SIZE
        runs = CGStorage().get_for_param(self.cache, 'size')
        sizes = [CGPlotter.convert_to_bit_str(s) for s in config.CACHE_PARAMS[self.cache]['SIZES']]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, r.summary) for r in runs]
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))

        self.axs[0].plot(sizes, miss_rates, 's-r')
        self.axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[0].set_title('size')
        self.axs[0].grid()

        # ASSOC
        runs = CGStorage().get_for_param(self.cache, 'assoc')
        sizes = [r.get_specs()[self.cache]['assoc'] for r in runs]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, r.summary) for r in runs]
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))

        self.axs[1].plot(sizes, miss_rates, 's-r')
        self.axs[1].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[1].set_title('set-associativity')
        self.axs[1].grid()

        # LINE
        runs = CGStorage().get_for_param(self.cache, 'line_size')
        sizes = [r.get_specs()[self.cache]['line_size'] + 'B' for r in runs]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, r.summary) for r in runs]
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))

        self.axs[2].plot(sizes, miss_rates, 's-r')
        self.axs[2].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[2].set_title('line size')
        self.axs[2].grid()

        min_miss_rate = floor(min(self.min_miss_rates))
        max_miss_rate = ceil(max(self.max_miss_rates))
        self.axs[0].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[1].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[2].set_ylim([min_miss_rate, max_miss_rate])

        self.axs[0].set_ylabel(f'{self.cache} r+w miss rate')


class CGPlotter:
    @staticmethod
    def convert_to_bit_str(num_bits):
        if num_bits < (1024 * 1024):
            return str(int(num_bits / 1024)) + 'KB'
        return str(int(num_bits / (1024 * 1024))) + 'MB'

    @staticmethod
    def plot_func(cache, func):
        CGSingleFuncPlot(cache, func).plot()

    @staticmethod
    def plot_funcs(cache, funcs):
        CGMultiFuncPlot(cache, funcs).plot()

    @staticmethod
    def plot_global(cache):
        CGGlobalPlot(cache).plot()
