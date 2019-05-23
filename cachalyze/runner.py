from cachalyze.cganalyzer import CGAnalyzer
from cachalyze.cgplotter import CGSingleFuncPlot, CGPlotter
from cachalyze.cgrunner import CGAsyncRunner


def run():
    pass

    # CGSingleFuncPlot('D1', '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h:Optiver::Common::Internal::Logger::Get()').plot()

    # SINGLE RUN WITH DEFAULT CONFIG
    # runner = CGRunner(CGRunConf())
    # print(runner.run())

    # RUN AND SAVE CG OUTPUT
    # CGAsyncRunner.run()

    # PLOT STATISTICS
    # CGPlotter().plot_func_d1(
    #     '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h:Optiver::Common'
    #     '::Internal::Logger::Get()',
    #     CGAnalyzer.total_misses_d1)
    # plot_func_ll('test',
    #              '/home/dennisspaan/Workspace/test/x_common_libs/libs/platform/../logging/logger.h:Optiver::Common::Internal::Logger::Get()',
    #              CGAnalyzer.total_misses_ll)
    CGPlotter().plot_app_d1(CGAnalyzer.total_misses_d1)
    CGPlotter().plot_app_ll(CGAnalyzer.total_misses_ll)
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
