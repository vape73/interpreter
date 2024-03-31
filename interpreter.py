import random
from expressions import Expressions
from for_loop_context import ForLoopContext
from source import Source
from variables import Variables
from line_scanner import LineScanner
from line_parser import LineParser
import time

commands = ["PRINT", "LET", "IF", "GOTO", "INPUT", "END", "CLEAR", "LIST", "LOAD", "SAVE", "GOSUB", "RETURN", "INPUT", "REM", "FOR", "NEXT"]

class Interpreter:
    MAX_STACK_LENGTH = 100
        
    def __init__(self, source: Source, variables: Variables, expressions: Expressions):
        self.stack = []
        self.source = source
        self.variables = variables
        self.expressions = expressions
        self.running = True
        self.current_line_number = None
        self.for_loops_stack = []

    def execute_line(self, line):
        try:
            scanner = LineScanner(line)
            parser = LineParser(scanner)
            self.expressions.set_scanner(scanner)
            self.expressions.set_parser(parser)
            command = scanner.getStrings(commands)
            
            scanner.getSpaces()
            if command == "LET":
                var = parser.getVariable()
                scanner.getChars("=")
                expression = self.expressions.get_expression()
                self.variables.set(var, expression)
            elif command == "PRINT":
                self.PRINT(parser, scanner)
            elif command == "IF":
                self.IF(scanner)
            elif command == "INPUT":
                self.INPUT(scanner, parser)
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
            elif command == "GOTO":
                label = scanner.getNumber()
                self.GOTO(label)
            elif command == "GOSUB":
                label = scanner.getNumber()
                self.GOSUB(label)
            elif command == "RETURN":
                self.RETURN()
            elif command == "REM":
                self.REM()
            elif command == "FOR":
                self.FOR(parser, scanner)
            elif command == "NEXT":
                self.NEXT()
            else:
                print(f"Unknown command or not implemented: {command}")
        except Exception as  e:
            print(f'ОШИБКА: {e} - {scanner.line} position: {scanner.pos}',)
            self.running = False

    def CLEAR(self):
        self.source.clear()
        self.variables.reset()

    def REM(self):
        pass

    def LIST(self):
        for num, line in self.source.lines.items():
            print(num, line)

    def LOAD(self, filename):
        self.source.load(filename)

    def SAVE(self, filename):
        self.source.save(filename)

    def END(self):
        self.running = False

    def INPUT(self, scanner, parser):
        while not scanner.isEOL():
            scanner.getSpaces()
            var_name = parser.getVariable()
            if var_name:
                try:
                    value = input(f"{var_name}? ")
                    self.variables.set(var_name, int(value))
                except ValueError:
                    print(f"Ошибка: введённое значение для переменной '{var_name}' не является числом.")
                    return
            if scanner.peekChar() == ',':
                scanner.shift()

    def PRINT(self, parser: LineParser, scanner: LineScanner):
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
            else:
                result = self.expressions.get_expression()
                print(result, end='')
                newline = True

        if newline:
            print()

    def IF(self, scanner: LineScanner):
        condition = self.expressions.get_comparison()
        scanner.getSpaces()
        then_part = scanner.getString("THEN")
        if then_part:
            rest_of_line = scanner.line[scanner.pos:].strip()
            else_index = rest_of_line.upper().find("ELSE")
            if condition:
                if else_index != -1:
                    self.execute_line(rest_of_line[:else_index].strip())
                else:
                    self.execute_line(rest_of_line.strip())
            else:
                if else_index != -1:
                    rest_of_line = rest_of_line[else_index + len("ELSE")+1:].strip()
                    self.execute_line(rest_of_line)

    def GOTO(self, label):
        if label in self.source.lines.keys():
            self.current_line_number = label
            current_line = self.source.get_line(self.current_line_number).strip()
            self.execute_line(current_line)
        else:
            raise Exception(f"Метка {label} не найдена")

    def GOSUB(self, label):
        if len(self.stack) < self.MAX_STACK_LENGTH:
            self.stack.append(self.current_line_number)
            self.GOTO(label)
        else:
            raise Exception('Переполнение стека')

    def RETURN(self):
        if self.stack:
            self.current_line_number = self.stack.pop()
        else:
            raise Exception('Возврат без GOSUB')
        
    def FOR(self, parser: LineParser, scanner: LineScanner):
        var = parser.getVariable()
        scanner.getChar('=')
        start = self.expressions.get_expression()
        scanner.getSpaces()
        if not scanner.getString("TO"):
            raise ValueError("Ожидается TO после начального значения цикла FOR")
        scanner.getSpaces()
        end = self.expressions.get_expression()
        scanner.getSpaces()
        step = 1
        if scanner.getString("STEP"):
            scanner.getSpaces()
            step = self.expressions.get_expression()
        self.variables.set(var, start)
        self.for_loops_stack.append(ForLoopContext(var, start, end, step, self.current_line_number))

    def NEXT(self):
        if not self.for_loops_stack:
            raise Exception("Нет активного цикла FOR для NEXT")
        context = self.for_loops_stack[-1]
        current_value = self.variables.get(context.var) + context.step
        if (context.step > 0 and current_value > context.end) or (context.step < 0 and current_value < context.end):
            self.for_loops_stack.pop() 
        else:
            self.variables.set(context.var, current_value)
            self.current_line_number = context.line_number 
    
    def run(self, start_from=None):
        self.running = True

        self.current_line_number = self.source.get_first_line_number() if not start_from else start_from

        while self.running and self.current_line_number is not None:
            current_line = self.source.get_line(self.current_line_number).strip()
            self.execute_line(current_line)
            
            if self.running:
                self.current_line_number = self.source.get_next_line_number(self.current_line_number)
