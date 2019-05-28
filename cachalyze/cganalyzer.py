import re
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


class CGGlobalAnalyzer:
    def __init__(self, outputs):
        self.outputs = outputs

    def filter_funcs(self, funcs):
        if config.INCLUDE_FOLDER:
            funcs = list(filter(lambda f: re.match(f'^{config.INCLUDE_FOLDER}', str(f)), funcs))
        else:
            if not config.INCLUDE_STANDARD_METHODS:
                funcs = list(filter(lambda f: not str(f).startswith('???'), funcs))

        return funcs

    def get_single_filtered_funcs(self):
        funcs = self.outputs[0].get_functions()
        return self.filter_funcs(funcs)

    def get_all_filtered_funcs(self):
        funcs = [f for output in self.outputs for f in output.get_functions()]
        return self.filter_funcs(funcs)

    def get_thresholded_functions(self):
        filtered_funcs = []
        unfiltered_funcs = sorted(self.get_single_filtered_funcs(), reverse=True, key=lambda f: f.events.Ir)
        total_instr = sum(f.events.Ir for f in unfiltered_funcs)
        curr_instr = 0

        while curr_instr / total_instr * 100 < config.THRESHOLD:
            func = unfiltered_funcs.pop(0)
            filtered_funcs.append(func)
            curr_instr += func.events.Ir

        return filtered_funcs

    def get_functions_by_change(self, cache, pre_def_funcs=[]):
        funcs = self.get_all_filtered_funcs()
        grouped_functions = {}

        for f in funcs:
            if pre_def_funcs:
                if f not in pre_def_funcs:
                    continue
            if str(f) in grouped_functions:
                grouped_functions[str(f)].append(f)
            else:
                grouped_functions[str(f)] = [f]

        results = {}

        for f in grouped_functions.keys():
            results[str(f)] = self._get_change_factor(cache, grouped_functions[str(f)])

        sorted_results = sorted(results.items(), reverse=True, key=lambda kv: kv[1])

        return [r[0] for r in sorted_results]

    def _get_change_factor(self, cache, funcs):
        funcs = list(map(lambda f: CGAnalyzer.get_count_for_cache(cache, f.events), funcs))
        diffs = numpy.diff(funcs)
        return sum([abs(d) for d in diffs])
