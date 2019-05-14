from itertools import groupby

import numpy


class CGAnalyzer:
    THRESHOLD = 99

    def __init__(self, cgoutput):
        self.output = cgoutput

    def get_thresholded_functions(self):
        thresholded_functions = []
        threshold = self.output.summary.Ir / 100 * self.THRESHOLD

        # TODO: Make event variable to sort by configurable
        functions = self.output.get_functions()
        functions.sort(key=lambda func: func.events.Ir, reverse=True)

        for function in functions:
            threshold -= function.events.Ir
            thresholded_functions.append(function)
            if threshold <= 0:
                return thresholded_functions


class CGGlobalAnalyzer:
    def __init__(self, outputs):
        self.outputs = outputs

    def get_functions_by_change(self):
        functions = [f for output in self.outputs for f in output.get_functions()]
        grouped_functions = {}

        for f in functions:
            if str(f) in grouped_functions:
                grouped_functions[str(f)].append(f)
            else:
                grouped_functions[str(f)] = [f]

        # TODO: sorteren op change_factor

        # functions.sort(key=lambda func: self._get_change_factor(func), reverse=True)
        return functions

    def _get_change_factor(self, funcs):
        funcs = list(map(lambda f: self.total_misses_d1(f.events), funcs))
        diffs = numpy.diff(funcs)
        return sum([abs(d) for d in diffs])

    def total_misses_d1(self, events):
        if events.Dr + events.Dw == 0:
            return 0
        return (events.D1mr + events.D1mw) / (events.Dr + events.Dw) * 10
