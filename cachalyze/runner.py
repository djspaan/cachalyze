# from cachalyze import config
from cachalyze.cganalyzer import CGGlobalAnalyzer, CGAnalyzer, CGFuncMapper
# from cachalyze.cgparser import CGParser
from cachalyze.cgplotter import CGPlotter
from cachalyze.cgrunner import CGAsyncRunner, CGRunConf
from cachalyze.cgstorage import CGStorage


def run():
    pass
    CGFuncMapper().fill_mapping(CGStorage().get_for_run_conf(CGRunConf()))

    # PLOT STATS PER LINE
    # func = output.get_func(CGFuncMapper().get_func(67))
    # lines = [l for l in func.lines.values() if l.number in [151, 141, 145, 142, 137]]
    # for l in lines:
    #     print(f'{l.number} & {l.events.format()} \\\\')

    # PLOT SINGLE FUNC
    # func = CGFuncMapper().get_func(67)
    # CGPlotter.plot_func('LL', func)

    # PLOT MOST CHANGING LINES FOR FUNCTION
    # outputs = CGStorage().get_for_program()
    # analyser = CGGlobalAnalyzer(outputs)
    # func = output.get_func(CGFuncMapper().get_func(67))
    # pre_def_lines = analyser.get_thresholded_lines_for_func(func)
    # pre_def_lines = [l.number for l in pre_def_lines]
    # ch_lines = analyser.get_lines_by_change_for_func('LL', func, pre_def_lines)
    # CGPlotter.plot_lines('LL', func, ch_lines)

    # ?
    # funcs = CGFuncMapper().get_funcs([59, 80, 75, 53, 38, 39, 41])
    # fil_funcs = [f for f in output.get_funcs() if str(f) in funcs]
    # sor_funcs = sorted(fil_funcs, reverse=True, key=lambda f: f.events.Ir)
    #
    # for f in sor_funcs:
    #     print(f'{CGFuncMapper().get_mapping(f)} & {f.events.format()} \\\\')

    # func = CGFuncMapper().get_func(38)
    # CGPlotter.plot_func('D1', func)

    # f = CGFuncMapper().get_func(38)
    # f = output.get_func(f)
    # file = f.file
    # for line, content, events in file.get_lines_with_events():
    #     print('{} {} {}'.format(line, events.format(), content))
    # quit()

    # analyzer = CGGlobalAnalyzer([output])
    # thres_funcs = analyzer.get_thresholded_functions()
    # outputs = CGStorage().get_for_program()
    # analyser = CGGlobalAnalyzer(outputs)
    # ch_funcs = analyser.get_functions_by_change('D1', thres_funcs)

    # f = output.get_func(ch_funcs[1])
    # file = f.file
    # for line, content, events in file.get_lines_with_events():
    #     print('{} {} {}'.format(line, events.format(), content))

    # funcs = sorted(thres_funcs, reverse=True, key=lambda f: (f.events.D1mr + f.events.D1mw + f.events.DLmr + f.events.DLmw) / (f.events.Dr + f.events.Dw))
    # for f in funcs:
    #     print(f'{CGFuncMapper().get_mapping(f)} & {f.events.format()}')

    # outputs = CGStorage().get_for_program()
    # analyser = CGGlobalAnalyzer(outputs)
    # ch_funcs = analyser.get_functions_by_change('D1', thres_funcs)
    # CGPlotter.plot_funcs('D1', ch_funcs[:10])
    # for f in ch_funcs:
    #     print(f'{CGFuncMapper().get_mapping(f)} - {f}')

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

    # PLOT MOST CHANGING (AND FILTER) FUNCTIONS
    # outputs = CGStorage().get_for_program()
    # analyser = CGGlobalAnalyzer(outputs)
    # thres_funcs = analyser.get_thresholded_funcs()
    # ch_funcs = analyser.get_functions_by_change('D1', thres_funcs)
    # fil_ch_funcs = analyser.filter_callees(outputs[0], ch_funcs)
    # for f in fil_ch_funcs:
    #     print(f'{CGFuncMapper().get_mapping(f)} - {f}')
    # CGPlotter.plot_funcs('D1', fil_ch_funcs)

    # PRINT LINES WITH EVENTS
    # print(file.path)
    # for event in output.events:
    #     print('{:>11}'.format(event), end='')
    # print('')
    # for line, content, events in file.get_lines_with_events():
    #     print('{} {} {}'.format(line.number, events.format(), content))
