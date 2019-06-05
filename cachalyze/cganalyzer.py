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

    @staticmethod
    def filter_funcs(funcs):
        if config.INCLUDE_FOLDER:
            funcs = list(filter(lambda f: re.match(f'^{config.INCLUDE_FOLDER}', str(f)), funcs))
        else:
            if not config.INCLUDE_STANDARD_METHODS:
                funcs = list(filter(lambda f: not str(f).startswith('???'), funcs))

        return funcs

    def get_single_filtered_funcs(self):
        funcs = self.outputs[0].get_funcs()
        return self.filter_funcs(funcs)

    def get_all_filtered_funcs(self):
        funcs = [f for output in self.outputs for f in output.get_funcs()]
        return self.filter_funcs(funcs)

    def get_thresholded_funcs(self):
        filtered_funcs = []
        unfiltered_funcs = sorted(self.get_single_filtered_funcs(), reverse=True,
                                  key=lambda f: f.events.Dr + f.events.Dw)
        total = sum(f.events.Dr + f.events.Dw for f in unfiltered_funcs)
        curr = 0

        while curr / total * 100 < config.THRESHOLD:
            func = unfiltered_funcs.pop(0)
            filtered_funcs.append(func)
            curr += func.events.Dr
            curr += func.events.Dw

        return filtered_funcs

    def get_thresholded_lines_for_func(self, func):
        """
        Takes the lines with the most cache misses of a function till LINE_THRESHOLD is reached.
        Works only for the lines of the function param given.

        :param func: CGFunction
        :return: [CGLine]
        """
        filtered_lines = []
        unfiltered_lines = sorted(func.lines.values(), reverse=True,
                                  key=lambda l: l.events.Dr + l.events.Dw)
        total = sum(l.events.Dr + l.events.Dw for l in unfiltered_lines)
        curr = 0

        while curr / total * 100 < config.LINE_THRESHOLD:
            line = unfiltered_lines.pop(0)
            filtered_lines.append(line)
            curr += line.events.Dr
            curr += line.events.Dw

        return filtered_lines

    def get_functions_by_change(self, cache, pre_def_funcs=[]):
        funcs = self.get_all_filtered_funcs()
        pre_def_funcs = [str(f) for f in pre_def_funcs]
        grouped_functions = {}

        for f in funcs:
            if pre_def_funcs:
                if str(f) not in pre_def_funcs:
                    continue
            if str(f) in grouped_functions:
                grouped_functions[str(f)].append(f)
            else:
                grouped_functions[str(f)] = [f]

        results = {}

        for f in grouped_functions.keys():
            results[str(f)] = self._get_change_factor(cache, grouped_functions[str(f)])

        sorted_results = sorted(results.items(), reverse=True, key=lambda kv: kv[1])

        # PRINT CHANGE FACTORS
        # for k,v in sorted_results:
        #     print(f'{CGFuncMapper().get_mapping(k)} & {round(v,5)} \\\\')

        return [r[0] for r in sorted_results]

    def get_lines_by_change_for_func(self, cache, func, pre_def_lines=[]):
        """

        :param func: CGFunction
        :param cache: str elem of {"D1","LL"}
        :param pre_def_lines: [int]
        :return: [int]
        """
        funcs = [f for f in self.get_all_filtered_funcs() if str(f) == str(func)]
        lines = [l for f in funcs for l in f.lines.values()]
        grouped_lines = {}

        for l in lines:
            if pre_def_lines:
                if l.number not in pre_def_lines:
                    continue
            if l.number in grouped_lines:
                grouped_lines[l.number].append(l)
            else:
                grouped_lines[l.number] = [l]

        results = {}

        for l in grouped_lines.keys():
            results[l] = self._get_change_factor(cache, grouped_lines[l])

        sorted_results = sorted(results.items(), reverse=True, key=lambda kv: kv[1])

        # PRINT CHANGE FACTORS
        for k,v in sorted_results:
            print(f'{k} & {round(v,5)} \\\\')

        return [r[0] for r in sorted_results]

    def _get_change_factor(self, cache, regions):
        regions = list(map(lambda r: CGAnalyzer.get_count_for_cache(cache, r.events), regions))
        diffs = numpy.diff(regions)
        return sum([abs(d) for d in diffs])


class CGFuncMapper:
    __instance = None
    output = None
    mapping = {}

    def __new__(cls, **kwargs):
        if CGFuncMapper.__instance is None:
            CGFuncMapper.__instance = object.__new__(cls)
        return CGFuncMapper.__instance

    def fill_mapping(self, output):
        funcs = sorted(str(f) for f in output.get_funcs())
        for c, f in enumerate(funcs):
            self.mapping[f] = c

    def get_mapping(self, func):
        return self.mapping[str(func)]

    def get_func(self, mapping):
        for f, m in self.mapping.items():
            if m == mapping:
                return f

    def get_funcs(self, mappings):
        funcs = []
        for f, m in self.mapping.items():
            if m in mappings:
                funcs.append(f)
        return funcs
