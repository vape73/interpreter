import random
from expressions import Expressions
from source import Source
from variables import Variables
from line_scanner import LineScanner
from line_parser import LineParser


class Interpreter:
    def __init__(self, source: Source, variables: Variables, expressions: Expressions):
        self.source = source
        self.variables = variables
        self.expressions = expressions
        self.running = True

    def execute_line(self, line):
        scanner = LineScanner(line)
        parser = LineParser(scanner)
        command = scanner.getStrings(
            ["PRINT", "LET", "IF", "GOTO", "INPUT", "END", "CLEAR", "LIST", "LOAD", "SAVE", "GOSUB", "RETURN"])

        if command == "LET":
            var = parser.getVariable()
            scanner.getChars("=")  # Assume single char '=' follows LET
            expression = self.expressions.get_expression()
            self.variables.set(var, expression)
        elif command == "PRINT":
            self.PRINT()
        elif command == "IF":
            condition = self.expressions.get_expression()  # Simplified condition handling
            then_part = scanner.getStrings(["THEN"])
            if then_part and condition:
                self.execute_line(line[scanner.pos:])
        elif command == "GOTO":
            label = parser.getVariable()
            self.GOTO(label)
        elif command == "INPUT":
            var_list = line[scanner.pos:].split(',')
            self.INPUT(var_list)
        elif command == "END":
            self.END()
        elif command == "CLEAR":
            self.CLEAR()
        elif command == "LIST":
            self.LIST()
        elif command == "LOAD":
            filename = parser.getQuotedString()
            self.LOAD(filename)
        elif command == "SAVE":
            filename = parser.getQuotedString()
            self.SAVE(filename)
        elif command == "GOSUB":
            label = parser.getVariable()
            self.GOSUB(label)
        elif command == "RETURN":
            self.RETURN()
        else:
            print(f"Unknown command or not implemented: {command}")

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

    def PRINT(self, args, parser: LineParser, scanner: LineScanner):
        newline = True
        while not scanner.isEOL():
            ch = scanner.peekChar()
            if ch == ',':
                newline = False
                print('\t', end='')
                scanner.shift()
            elif ch == ';':
                newline = False
                print(' ', end='')
                scanner.shift()
            elif string := parser.getQuotedString():
                print(string, end='')
                newline = True
            else:  # arg is an expression
                result = self.expressions.get_expression()
                print(result, end='')
                newline = True

        if newline:
            print()

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