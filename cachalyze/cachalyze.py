from cachalyze.cganalyzer import CGFuncMapper
from cachalyze.cgplotter import CGPlotter
from cachalyze.cgrunner import CGAsyncRunner
from cachalyze.cgstorage import CGStorage
from cachalyze.config import Config
from cachalyze.logger import Logger

__version__ = '0.8.1'

import sys
import argparse


class RunSimCommand:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Run simulations for a given program')
        self._add_args()

    def is_power2(self, num):
        if num != 0 and ((num & (num - 1)) == 0):
            return num
        Logger.error('Cache parameters should be powers of two, i.e. x=2^n')

    def set_config(self):
        args = self.parser.parse_args(sys.argv[2:])
        Config.VERBOSE = args.verbose
        Config.PROGRAM_CMD = ' '.join(args.program)
        Config.PROGRAM_ALIAS = args.alias or args.program[0]
        Config.N_THREADS = args.n_threads
        Config.OUT_DIR = args.out_dir
        Config.OUT_PREFIX = args.out_prefix
        for ls in args.d1_line_sizes.split(',') + args.ll_line_sizes.split(','):
            if int(ls) < Config.REGISTER_SIZE:
                Logger.error(f'Line sizes can not be smaller than the register size ({Config.REGISTER_SIZE}B)')
        if not args.d1_all:
            Config.CACHE_PARAMS['D1']['SIZE'] = [self.is_power2(int(size)) for size in args.d1_sizes.split(',')]
            Config.CACHE_PARAMS['D1']['ASSOC'] = [self.is_power2(int(assoc)) for assoc in args.d1_assocs.split(',')]
            Config.CACHE_PARAMS['D1']['LINE_SIZE'] = [self.is_power2(int(ls)) for ls in args.d1_line_sizes.split(',')]
        if not args.ll_all:
            Config.CACHE_PARAMS['LL']['SIZE'] = [self.is_power2(int(size)) for size in args.ll_sizes.split(',')]
            Config.CACHE_PARAMS['LL']['ASSOC'] = [self.is_power2(int(assoc)) for assoc in args.ll_assocs.split(',')]
            Config.CACHE_PARAMS['LL']['LINE_SIZE'] = [self.is_power2(int(ls)) for ls in args.ll_line_sizes.split(',')]

    def run(self):
        CGAsyncRunner.run()

    def _add_args(self):
        optional_args = self.parser._action_groups.pop()
        required_args = self.parser.add_argument_group('required arguments')
        optional_args.add_argument('-v', '--verbose', help='whether to print run-time information', action='store_true',
                                   dest='verbose')
        optional_args.add_argument('-a', '--prog-alias', help='alias for the given program', action='store',
                                   dest='alias')
        optional_args.add_argument('--n-threads', help='number of threads to use for running simulations', type=int,
                                   default=2, action='store', dest='n_threads')
        optional_args.add_argument('--out-dir', help='output directory to store the callgrind output files in',
                                   default='.', action='store', dest='out_dir')
        optional_args.add_argument('--out-prefix', help='output prefix to prepend the callgrind output files with',
                                   default='callgrind.out', action='store', dest='out_prefix')
        optional_args.add_argument('--d1-all', help='simulate the D1 cache with the complete parameter space',
                                   action='store_true', dest='d1_all')
        optional_args.add_argument('--d1-sizes',
                                   help='first level data-cache sizes in bytes to use for the simulations,'
                                        ' where a size=2^n, in the format <size>,...,<size>',
                                   action='store', dest='d1_sizes', default='32768')
        optional_args.add_argument('--d1-assocs',
                                   help='first level data-cache set-associativities to use for the simulations,'
                                        ' where a assoc=2^n, in the format <assoc>,...,<assoc> ',
                                   action='store', dest='d1_assocs', default='8')
        optional_args.add_argument('--d1-line-sizes',
                                   help='first level data-cache line sizes in bytes to use for the simulations,'
                                        ' where a line_size=2^n, in the format <line_size>,...,<line_size> ',
                                   action='store', dest='d1_line_sizes', default='64')
        optional_args.add_argument('--ll-all', help='simulate the LL cache with the complete parameter space',
                                   action='store_true', dest='ll_all')
        optional_args.add_argument('--ll-sizes', help='last level cache sizes in bytes to use for the simulations,'
                                                      ' where a size=2^n, in the format <size>,...,<size>',
                                   action='store', dest='ll_sizes',
                                   default='8388608')
        optional_args.add_argument('--ll-assocs',
                                   help='last level cache set-associativities to use for the simulations,'
                                        ' where a assoc=2^n, in the format <assoc>,...,<assoc> ',
                                   action='store', dest='ll_assocs', default='16')
        optional_args.add_argument('--ll-line-sizes',
                                   help='last level cache line sizes in bytes to use for the simulations,'
                                        ' where a line_size=2^n, in the format <line_size>,...,<line_size> ',
                                   action='store', dest='ll_line_sizes', default='64')
        required_args.add_argument('program', help='command for the program', action='store', nargs=argparse.REMAINDER)
        self.parser._action_groups.append(optional_args)


class PlotCommand:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Plot the results of ran simulations')
        self._add_args()
        self.cache = 'D1'
        self.type = 'global'
        self.region = None

    def set_config(self):
        args = self.parser.parse_args(sys.argv[2:])
        self.cache = args.cache
        self.type = args.type
        self.region = args.region
        Config.VERBOSE = args.verbose
        Config.PROGRAM_ALIAS = args.alias
        Config.REGION_THRESHOLD = args.region_threshold
        Config.LINE_THRESHOLD = args.line_threshold
        Config.OUT_DIR = args.out_dir
        Config.OUT_PREFIX = args.out_prefix
        Config.INCLUDE_DIR = args.include_dir
        Config.INCLUDE_STANDARD_METHODS = args.include_standard_methods
        Config.SAVE_FIGURE = args.save_figure

    def run(self):
        CGFuncMapper().fill_mapping(CGStorage().get_for_program()[0])

        if self.type == 'regions':
            CGPlotter.plot_thresholded_most_changing_funcs(self.cache)
        elif self.type == 'region':
            CGPlotter.plot_func(self.cache, CGFuncMapper().get_func(self.region))
        elif self.type == 'region-lines':
            CGPlotter.plot_thresholded_most_changing_lines_for_func(self.cache, self.region)
        else:
            CGPlotter.plot_global(self.cache)

    def _add_args(self):
        optional_args = self.parser._action_groups.pop()
        required_args = self.parser.add_argument_group('required arguments')
        optional_args.add_argument('-v', '--verbose', help='whether to print run-time information', action='store_true',
                                   dest='verbose')
        required_args.add_argument('-a', '--prog-alias', help='alias for the given program', action='store',
                                   dest='alias', required=True)
        optional_args.add_argument('-c', '--cache', help='level of cache to plot for', action='store',
                                   dest='cache', default='D1', choices=['D1', 'LL'])
        optional_args.add_argument('-s', '--save-figure', help='whether to save the plot to an image',
                                   action='store_true', dest='save_figure')
        optional_args.add_argument('-t', '--type', help='type of plot',
                                   action='store', dest='type', default='global',
                                   choices=['global', 'regions', 'region', 'region-lines'])
        optional_args.add_argument('-r', '--region', help='region to plot, mandatory for type=region|region-lines',
                                   action='store', dest='region', type=int)
        optional_args.add_argument('--region-threshold', help='relative threshold to filter regions by', type=float,
                                   default=99.9, action='store', dest='region_threshold')
        optional_args.add_argument('--line-threshold', help='relative threshold to filter lines by', type=float,
                                   default=99.9, action='store', dest='line_threshold')
        optional_args.add_argument('--out-dir', help='output directory to retrieve the callgrind output files from',
                                   default='.', action='store', dest='out_dir')
        optional_args.add_argument('--out-prefix', help='output prefix of the prepended output files',
                                   default='callgrind.out', action='store', dest='out_prefix')
        optional_args.add_argument('--include-dir', help='source code directory to only be included in the analysis',
                                   default='', action='store', dest='include_dir')
        optional_args.add_argument('--use-backend', help='graphics backend to use for the generation of plots, '
                                                         'note that agg does only save to file, so be sure to add the '
                                                         '-s flag',
                                   default='tkinter', action='store', dest='backend', choices=['tkinter', 'agg'])
        optional_args.add_argument('--include-standard-methods', help='whether to include standard C functions \
                                  in the analysis', action='store_true', dest='include_standard_methods')
        self.parser._action_groups.append(optional_args)


class Cachalyze:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Analyze cache sensitivity for C/C++ programs.',
            usage=''' cachalyze <command> [<args>]
            
Available commands:
    runsim  Run simulations for a given program
    plot    Plot the results of ran simulations
''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def runsim(self):
        command = RunSimCommand()
        command.set_config()
        command.run()

    def plot(self):
        command = PlotCommand()
        command.set_config()
        command.run()


def main():
    Cachalyze()
