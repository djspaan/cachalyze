import re

from cachalyze import config
from cachalyze.cganalyzer import CGGlobalAnalyzer, CGAnalyzer
from cachalyze.cgparser import CGParser
from cachalyze.cgplotter import CGPlotter
from cachalyze.cgrunner import CGAsyncRunner, CGRunConf, RUN_CONFS
from cachalyze.cgstorage import CGStorage

REALISED_VOLS_FUNC_MAPPING = {}


def fill_mapping(output):
    funcs = sorted(str(f) for f in output.get_funcs())
    for c, f in enumerate(funcs):
        REALISED_VOLS_FUNC_MAPPING[f] = c


def get_mapping(func):
    return REALISED_VOLS_FUNC_MAPPING[str(func)]


def run():
    pass

    # output = CGStorage().get_for_run_conf(CGRunConf())
    # fill_mapping(output)
    # analyzer = CGGlobalAnalyzer([output])
    # thres_funcs = analyzer.get_thresholded_functions()

    # funcs = sorted(thres_funcs, reverse=True, key=lambda f: (f.events.D1mr + f.events.D1mw + f.events.DLmr + f.events.DLmw) / (f.events.Dr + f.events.Dw))
    # for f in funcs:
    #     print(f'{get_mapping(f)} & {f.events.format()}')

    # outputs = CGStorage().get_for_program()
    # analyser = CGGlobalAnalyzer(outputs)
    # ch_funcs = analyser.get_functions_by_change('D1', thres_funcs)
    # CGPlotter.plot_funcs('LL', ch_funcs[:10])
    # for f in ch_funcs:
    #     print(f'{f}')

    # funcs = sorted(funcs, reverse=True, key=lambda f: count_func(output.summary, f))
    # funcs = analyzer.get_functions_by_change('D1', funcs)
    # print(funcs)
    # for f in funcs:
    #     print(f)

    # PRINT THRESHOLDED FUNCTIONS
    # output = CGParser('/home/dennisspaan/Workspace/cachalyze/out/cgrunner.out.test.32768,8,64.8388608,16,64').parse()
    # funcs = CGAnalyzer(output).get_thresholded_functions()
    # print(output.summary)
    # for f in funcs:
    #     print(f)

    # CGPlotter.plot_func('D1', '/home/dennisspaan/Workspace/test/libs/test/actions/calculations.cc:Optiver::RealisedVols::(anonymous namespace)::GenerateHedgepoints(double, unsigned long, unsigned long)')
    # 'CGPlotter.plot_funcs('D1',
    # ['/home/dennisspaan/Workspace/test/x_common_libs/libs/common/../common/timing.h:Optiver::TimeSpan
    # ::GetNanosecondsDouble() const', '/home/dennisspaan/Workspace/test/x_common_libs/libs/common/../common
    # /timing.h:Optiver::TimeSpan::GetNanosecondsDouble() const']) CGPlotter.plot_global('LL')

    # SINGLE RUN WITH DEFAULT CONFIG
    # runner = CGRunner(CGRunConf())
    # print(runner.run())

    # RUN AND SAVE CG OUTPUT
    # CGAsyncRunner.run()

    # PLOT STATISTICS
    # CGPlotter.plot_func('D1',
    #                     '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h'
    #                     ':Optiver::Common '
    #                     '::Internal::Logger::Get()')
    # CGPlotter.plot_func('LL',
    #                     '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h'
    #                     ':Optiver::Common '
    #                     '::Internal::Logger::Get()')
    # CGPlotter.plot_global('D1')
    # CGPlotter.plot_global('LL')
    # plot_funcs('D1', [])
    # plot_funcs('LL', [])

    # PRINT THRESHOLDED FUNCTIONS
    # output = CGParser('out/cgrunner.out.local_subscriber.32768,8,64.8388608,16,64').parse()
    # analyser = CGAnalyzer(output)
    # for func in analyser.get_thresholded_functions():
    #     print('{} {}'.format(func.events, func))

    # PRINT MOST CHANGING FUNCTIONS
    # outputs = CGStorage().get_for_program()
    # analyser = CGGlobalAnalyzer(outputs)
    # funcs = analyser.get_functions_by_change()
    # for f in funcs:
    #     print(f)
    # CGPlotter.plot_funcs('D1', funcs)

    # PRINT MOST CHANGING FUNCTIONS WITH MOST INSTRUCTIONS
    # outputs = CGStorage().get_for_program()
    # analyser = CGGlobalAnalyzer(outputs)
    # thres_funcs = analyser.get_thresholded_functions()
    # ch_funcs = analyser.get_functions_by_change('D1', thres_funcs)
    # for f in ch_funcs:
    #     print(f'{f}')
    # CGPlotter.plot_funcs('D1', ch_funcs[:10])

    # CGStorage().get_for_param('D1', 'SIZE')

    # PRINT LINES WITH EVENTS
    # print(file.path)
    # for event in output.events:
    #     print('{:>11}'.format(event), end='')
    # print('')
    # for line, content, events in file.get_lines_with_events():
    #     print('{} {}'.format(events.format(), content))
