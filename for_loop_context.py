class ForLoopContext:
    def __init__(self, var, start, end, step, line_number):
        self.var = var  # переменная цикла
        self.start = start  # начальное значение
        self.end = end  # конечное значение
        self.step = step  # шаг
        self.line_number = line_number  # номер строки с FOR, для возврата после NEXT
        self.iteration_complete = False  # флаг завершения итерации