from cachalyze.cgparser import CGParser
from cachalyze.cganalyzer import CGAnalyzer


def run():
    output = CGParser().parse("/home/dennis/Workspace/cachalyze/data/cachegrind.out.9696")
    analyzer = CGAnalyzer(output)
    funcs = analyzer.get_thresholded_functions()
    file = funcs[0].file

    # for func in output.get_functions():
    #     print('{} {}'.format(func.events, func))

    print(file.path)
    for event in output.events:
        print('{:>11}'.format(event), end='')
    print('')
    for line, content, events in file.get_lines_with_events():
        print('{} {}'.format(events.format(), content))
