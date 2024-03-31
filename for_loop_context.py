class ForLoopContext:
    def __init__(self, var, start, end, step, line_number):
        self.var = var
        self.start = start
        self.end = end
        self.step = step
        self.line_number = line_number
        self.iteration_complete = False