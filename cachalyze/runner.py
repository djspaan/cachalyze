from cachalyze.cgparser import CGParser
from cachalyze.cganalyzer import CGAnalyzer


def run():
    output = CGParser().parse("/home/dennis/Workspace/cachalyze/data/cachegrind.out.9696")
    analyzer = CGAnalyzer(output)
    funcs = analyzer.get_thresholded_functions()
    file = funcs[0].file
    print(file.path)
    for line, content, events in file.get_lines_with_events():
        print("{} {} {}".format(events, line, content))
