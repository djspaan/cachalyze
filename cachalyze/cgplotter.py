import os
from math import ceil, floor
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import cachalyze.config as config
from cachalyze.cganalyzer import CGGlobalAnalyzer, CGAnalyzer
from cachalyze.cgstorage import CGStorage
from cachalyze.cganalyzer import CGFuncMapper


class CGPlot:
    TYPE = 'undefined'

    def __init__(self, cache):
        self.cache = cache
        self.min_miss_rates = self.max_miss_rates = []
        self.fig, self.axs = plt.subplots(1, 3, figsize=(15, 4))

    def plot(self):
        self.plot_subplots()
        plt.tight_layout()
        if config.SAVE_FIGURE:
            file_name = f'{config.OUT_DIR}/{config.OUT_PREFIX}.{config.PROGRAM_ALIAS}_{self.TYPE}_{self.cache}.png'
            plt.savefig(file_name)

        plt.show()

    def plot_subplots(self):
        raise Exception('CGPlot class is not instantiatable.')


class CGSingleFuncPlot(CGPlot):
    TYPE = 'single_func'

    def __init__(self, cache, func):
        self.func = func
        super().__init__(cache)

    def plot_subplots(self):
        # SIZE
        runs = CGStorage().get_for_param(self.cache, 'SIZE')
        sizes = [CGPlotter.convert_to_bit_str(s) for s in config.CACHE_PARAMS[self.cache]['SIZE']]
        funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(self.func)]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        self.axs[0].plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))
        self.axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[0].set_title('size')

        self.axs[0].grid()

        # ASSOC
        runs = CGStorage().get_for_param(self.cache, 'ASSOC')
        sizes = [r.get_specs()[self.cache]['ASSOC'] for r in runs]
        funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(self.func)]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        self.axs[1].plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))
        self.axs[1].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[1].set_title('set-associativity')
        self.axs[1].grid()

        # LINE SIZE
        runs = CGStorage().get_for_param(self.cache, 'LINE_SIZE')
        sizes = [r.get_specs()[self.cache]['LINE_SIZE'] + 'B' for r in runs]
        funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(self.func)]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
        self.axs[2].plot(sizes, miss_rates, 's-', label=funcs[0].get_formatted_name())
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))
        self.axs[2].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[2].set_title('line size')
        self.axs[2].grid()

        min_miss_rate = floor(min(self.min_miss_rates))
        max_miss_rate = max(self.max_miss_rates)

        self.axs[0].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[1].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[2].set_ylim([min_miss_rate, max_miss_rate])

        self.axs[0].set_ylabel(f'{self.cache} r+w miss rate')


class CGMultiFuncPlot(CGPlot):
    TYPE = 'multiple_funcs'

    def __init__(self, cache, funcs):
        self.funcs = funcs
        super().__init__(cache)

    def plot_subplots(self):
        # SIZE
        runs = CGStorage().get_for_param(self.cache, 'SIZE')
        sizes = [CGPlotter.convert_to_bit_str(s) for s in config.CACHE_PARAMS[self.cache]['SIZE']]
        for gg, func in enumerate(self.funcs):
            funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(func)]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
            ls = ['-', '--', '-.', ':'][gg % 4]
            self.axs[0].plot(sizes, miss_rates, 's-', label=CGFuncMapper().get_mapping(str(funcs[0])), alpha=0.7, linestyle=ls)
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[0].set_title('size')
        self.axs[0].grid()
        self.axs[0].legend()

        # for l in self.axs[0].get_lines():
        #     print(f'{l.get_color()} - {l.get_label()}')

        # ASSOC
        runs = CGStorage().get_for_param(self.cache, 'ASSOC')
        sizes = [r.get_specs()[self.cache]['ASSOC'] for r in runs]
        for gg, func in enumerate(self.funcs):
            funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(func)]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
            ls = ['-', '--', '-.', ':'][gg % 4]
            self.axs[1].plot(sizes, miss_rates, 's-', alpha=0.7, linestyle=ls)
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[1].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[1].set_title('set-associativity')
        self.axs[1].grid()

        # LINE
        runs = CGStorage().get_for_param(self.cache, 'LINE_SIZE')
        sizes = [r.get_specs()[self.cache]['LINE_SIZE'] + 'B' for r in runs]
        for gg, func in enumerate(self.funcs):
            funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(func)]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, f.events) for f in funcs]
            ls = ['-', '--', '-.', ':'][gg % 4]
            self.axs[2].plot(sizes, miss_rates, 's-', alpha=0.7, linestyle=ls)
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[2].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[2].set_title('line size')
        self.axs[2].grid()

        min_miss_rate = floor(min(self.min_miss_rates))
        max_miss_rate = max(self.max_miss_rates)
        self.axs[0].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[1].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[2].set_ylim([min_miss_rate, max_miss_rate])

        self.axs[0].set_ylabel(f'{self.cache} r+w miss rate')


class CGMultiLinePlot(CGPlot):
    TYPE = 'reg_lines'

    def __init__(self, cache, func, lines):
        self.func = func
        self.lines = lines
        super().__init__(cache)

    def plot_subplots(self):
        # SIZE
        runs = CGStorage().get_for_param(self.cache, 'SIZE')
        sizes = [CGPlotter.convert_to_bit_str(s) for s in config.CACHE_PARAMS[self.cache]['SIZE']]
        for gg, line in enumerate(self.lines):
            funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(self.func)]
            lines = [l for f in funcs for l in f.lines.values() if l.number == line]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, l.events) for l in lines]
            ls = ['-', '--', '-.', ':'][gg % 4]
            self.axs[0].plot(sizes, miss_rates, 's-', label=str(line), alpha=0.7, linestyle=ls)
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[0].set_title('size')
        self.axs[0].grid()
        self.axs[0].legend()

        # ASSOC
        runs = CGStorage().get_for_param(self.cache, 'ASSOC')
        sizes = [r.get_specs()[self.cache]['ASSOC'] for r in runs]
        for gg, line in enumerate(self.lines):
            funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(self.func)]
            lines = [l for f in funcs for l in f.lines.values() if l.number == line]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, l.events) for l in lines]
            ls = ['-', '--', '-.', ':'][gg % 4]
            self.axs[1].plot(sizes, miss_rates, 's-', label=str(line), alpha=0.7, linestyle=ls)
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[1].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[1].set_title('set-associativity')
        self.axs[1].grid()

        # LINE
        runs = CGStorage().get_for_param(self.cache, 'LINE_SIZE')
        sizes = [r.get_specs()[self.cache]['LINE_SIZE'] + 'B' for r in runs]
        for gg, line in enumerate(self.lines):
            funcs = [f for r in runs for f in r.get_funcs() if str(f) == str(self.func)]
            lines = [l for f in funcs for l in f.lines.values() if l.number == line]
            miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, l.events) for l in lines]
            ls = ['-', '--', '-.', ':'][gg % 4]
            self.axs[2].plot(sizes, miss_rates, 's-', label=str(line), alpha=0.7, linestyle=ls)
            self.min_miss_rates.append(min(miss_rates))
            self.max_miss_rates.append(max(miss_rates))

        self.axs[2].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[2].set_title('line size')
        self.axs[2].grid()

        min_miss_rate = floor(min(self.min_miss_rates))
        max_miss_rate = max(self.max_miss_rates)
        self.axs[0].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[1].set_ylim([min_miss_rate, max_miss_rate])
        self.axs[2].set_ylim([min_miss_rate, max_miss_rate])

        self.axs[0].set_ylabel(f'{self.cache} r+w miss rate')


class CGGlobalPlot(CGPlot):
    TYPE = 'global'

    def plot_subplots(self):
        # SIZE
        runs = CGStorage().get_for_param(self.cache, 'SIZE')
        sizes = [CGPlotter.convert_to_bit_str(s) for s in config.CACHE_PARAMS[self.cache]['SIZE']]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, r.summary) for r in runs]
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))

        self.axs[0].plot(sizes, miss_rates, 's-r')
        self.axs[0].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[0].set_title('size')
        self.axs[0].grid()

        # ASSOC
        runs = CGStorage().get_for_param(self.cache, 'ASSOC')
        sizes = [r.get_specs()[self.cache]['ASSOC'] for r in runs]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, r.summary) for r in runs]
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))

        self.axs[1].plot(sizes, miss_rates, 's-r')
        self.axs[1].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[1].set_title('set-associativity')
        self.axs[1].grid()

        # LINE
        runs = CGStorage().get_for_param(self.cache, 'LINE_SIZE')
        sizes = [r.get_specs()[self.cache]['LINE_SIZE'] + 'B' for r in runs]
        miss_rates = [CGAnalyzer.get_count_for_cache(self.cache, r.summary) for r in runs]
        self.min_miss_rates.append(min(miss_rates))
        self.max_miss_rates.append(max(miss_rates))

        self.axs[2].plot(sizes, miss_rates, 's-r')
        self.axs[2].yaxis.set_major_formatter(ticker.PercentFormatter())
        self.axs[2].set_title('line size')
        self.axs[2].grid()

        min_miss_rate = floor(min(self.min_miss_rates))
        max_miss_rate = max(self.max_miss_rates)
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
    def plot_lines(cache, func, lines):
        CGMultiLinePlot(cache, func, lines).plot()

    @staticmethod
    def plot_global(cache):
        CGGlobalPlot(cache).plot()
