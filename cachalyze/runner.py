from cachalyze.cgparser import CGParser
from cachalyze.cganalyzer import CGAnalyzer


def run():
    output = CGParser().parse("/home/dennis/Workspace/cachalyze/data/cachegrind.out.16397")
    analyzer = CGAnalyzer(output)
    funcs = analyzer.get_thresholded_functions()
