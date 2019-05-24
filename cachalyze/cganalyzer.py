import numpy

from cachalyze import config


class CGAnalyzer:
    def __init__(self, output):
        self.output = output

    @staticmethod
    def total_misses_d1(events):
        if events.Dr + events.Dw == 0:
            return 0
        return (events.D1mr + events.D1mw) / (events.Dr + events.Dw) * 100

    @staticmethod
    def read_misses_d1(events):
        if events.Dr == 0:
            return 0
        return events.D1mr / events.Dr * 100

    @staticmethod
    def write_misses_d1(events):
        if events.Dw == 0:
            return 0
        return events.D1mw / events.Dw * 100

    @staticmethod
    def total_misses_ll(events):
        if events.Dr + events.Dw == 0:
            return 0
        return (events.DLmr + events.DLmw) / (events.Dr + events.Dw) * 100

    @staticmethod
    def read_misses_ll(events):
        if events.Dr == 0:
            return 0
        return events.DLmr / events.Dr * 100

    @staticmethod
    def write_misses_ll(events):
        if events.Dw == 0:
            return 0
        return events.DLmw / events.Dw * 100

    @staticmethod
    def get_count_for_cache(cache, events):
        if cache == 'D1':
            return CGAnalyzer.total_misses_d1(events)
        if cache == 'LL':
            return CGAnalyzer.total_misses_ll(events)

    def get_thresholded_functions(self):
        thresholded_functions = []
        threshold = self.output.summary.Ir / 100 * config.THRESHOLD

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

    def get_functions_by_change(self, pre_def_funcs=[]):
        functions = [f for output in self.outputs for f in output.get_functions()]
        grouped_functions = {}

        for f in functions:
            if pre_def_funcs:
                if f not in pre_def_funcs:
                    continue
            if not config.INCLUDE_STANDARD_METHODS:
                if str(f).startswith('???'):
                    continue
            if str(f) in grouped_functions:
                grouped_functions[str(f)].append(f)
            else:
                grouped_functions[str(f)] = [f]

        results = {}

        for f in grouped_functions.keys():
            results[str(f)] = self._get_change_factor(grouped_functions[str(f)])

        sorted_results = sorted(results.items(), reverse=True, key=lambda kv: kv[1])

        return [r[0] for r in sorted_results]

    def _get_change_factor(self, funcs):
        funcs = list(map(lambda f: CGAnalyzer.total_misses_d1(f.events), funcs))
        diffs = numpy.diff(funcs)
        return sum([abs(d) for d in diffs])
