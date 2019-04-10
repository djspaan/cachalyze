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
