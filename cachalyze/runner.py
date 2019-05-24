import re

from cachalyze import config
from cachalyze.cganalyzer import CGGlobalAnalyzer, CGAnalyzer
from cachalyze.cgparser import CGParser
from cachalyze.cgplotter import CGPlotter
from cachalyze.cgrunner import CGAsyncRunner
from cachalyze.cgstorage import CGStorage


def run():
    pass

    # PRINT THRESHOLDED FUNCTIONS
    # output = CGParser('/home/dennisspaan/Workspace/cachalyze/out/cgrunner.out.test.32768,8,64.8388608,16,64').parse()
    # funcs = CGAnalyzer(output).get_thresholded_functions()
    # print(output.summary)
    # for f in funcs:
    #     print(f)


    # CGPlotter.plot_single_func('LL', '/home/dennisspaan/Workspace/test/x_common_libs/libs/common/../common
    # /timing.h:Optiver::TimeSpan::GetNanosecondsDouble() const') CGPlotter.plot_funcs('D1',
    # ['/home/dennisspaan/Workspace/test/x_common_libs/libs/common/../common/timing.h:Optiver::TimeSpan
    # ::GetNanosecondsDouble() const', '/home/dennisspaan/Workspace/test/x_common_libs/libs/common/../common
    # /timing.h:Optiver::TimeSpan::GetNanosecondsDouble() const']) CGPlotter.plot_global('LL')

    # SINGLE RUN WITH DEFAULT CONFIG
    # runner = CGRunner(CGRunConf())
    # print(runner.run())

    # RUN AND SAVE CG OUTPUT
    CGAsyncRunner.run()

    # PLOT STATISTICS
    # CGPlotter().plot_func_d1(
    #     '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h:Optiver::Common'
    #     '::Internal::Logger::Get()',
    #     CGAnalyzer.total_misses_d1)
    # plot_func_ll('test',
    #              '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h:Optiver::Common::Internal::Logger::Get()',
    #              CGAnalyzer.total_misses_ll)
    # CGPlotter().plot_app_d1(CGAnalyzer.total_misses_d1)
    # CGPlotter().plot_app_ll(CGAnalyzer.total_misses_ll)
    # plot_funcs_d1('test', CGAnalyzer.total_misses_d1)
    # plot_funcs_ll('test', CGAnalyzer.total_misses_ll)

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

    # PRINT FUNCTIONS WITH MOST INSTRUCTIONS
    # outputs = CGStorage().get_for_program()
    # analyser = CGGlobalAnalyzer(outputs)
    # output = outputs[4]
    # funcs = output.get_functions()
    # sor_funcs = sorted(funcs, reverse=True, key=lambda f: f.events.Ir)
    # ch_funcs = analyser.get_functions_by_change(sor_funcs[:1000])
    #
    # CGPlotter.plot_funcs('D1', ch_funcs[:5])
    # for f in sor_funcs:
    #     if re.match('^/home/dennisspaan/Workspace/test/lib', str(f)):
    #         print(f'{f.events.Ir} {f}')

    # analyser = CGGlobalAnalyzer(outputs)
    # funcs = analyser.get_functions_by_change()[:5]
    # CGPlotter.plot_funcs('D1', funcs)

    # for func in analyser.get_thresholded_functions():
    #     print('{} {}'.format(func.events, func))

    # PRINT LINES WITH EVENTS
    # print(file.path)
    # for event in output.events:
    #     print('{:>11}'.format(event), end='')
    # print('')
    # for line, content, events in file.get_lines_with_events():
    #     print('{} {}'.format(events.format(), content))
