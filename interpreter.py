import random
from source import Source
from variables import Variables
from expressions import Expressions

class Interpreter:
    MAX_STACK_LENGTH = 100

    def __init__(self, variables: Variables, expressions: Expressions):
        self.source = Source()
        self.variables = variables
        self.expressions = expressions
        self.stack = []
        self.running = True

    def execute_line(self, line):
        # Разбор и выполнение команды в строке
        pass

    def run(self, start_label=None):
        # Запуск программы с опциональным начальным меткой
        if start_label is not None:
            if not self.source._find(start_label):
                print("Label not found.")
                return
        else:
            self.source.gotoNext()

        while self.running and not self.source.isEOL():
            line = self.source.getCurrentLine()
            self.execute_line(line)
            if not self.source.gotoNext():
                break

    def CLEAR(self):
        self.source.clear()
        self.variables.reset()

    def REM(self):
        # Этот оператор просто игнорирует все до конца строки
        pass

    def LIST(self):
        for line in self.source.lines:
            print(line)

    def LOAD(self, filename):
        self.source.load(filename)

    def SAVE(self, filename):
        self.source.save(filename)

    def GOTO(self, label):
        if not self.source._find(label):
            print(f"Label {label} not found.")
            self.running = False

    def END(self):
        self.running = False

    def INPUT(self, var_list):
        for var in var_list.split(","):
            value = input(f"{var.strip()}? ")
            self.variables.set(var.strip(), int(value))

    def PRINT(self, expr_list):
        # Реализуйте вывод согласно заданию
        pass

    def LET(self, var, expression):
        # Реализуйте вычисление выражения и присваивание значения переменной
        pass

    def IF(self, condition):
        # Реализуйте условное выполнение
        pass

    def GOSUB(self, label):
        if len(self.stack) < self.MAX_STACK_LENGTH:
            self.stack.append((self.source.lineNo, self.source.lineIdx))
            self.GOTO(label)
        else:
            print("Stack overflow.")
            self.running = False

    def RETURN(self):
        if self.stack:
            lineNo, lineIdx = self.stack.pop()
            self.source.lineNo = lineNo
            self.source.lineIdx = lineIdx
            self.source.gotoNext()
        else:
            print("Return without GOSUB.")
            self.running = False

    def RND(self):
        """Вычисляет выражение и возвращает случайное число от 0 до этого значения."""
        expression_result = self.expressions.get_expression()
        return random.randint(0, max(0, expression_result - 1))