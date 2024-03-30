import random
from line_parser import LineParser
from line_scanner import LineScanner
from variables import Variables

class Expressions:
    def __init__(self, variables: Variables):
        self.variables = variables
        self.scanner = None
        self.parser = None

    def set_scanner(self, scanner: LineScanner):
        self.scanner = scanner
        
    def set_parser(self, parser: LineParser):
        self.parser = parser

    def get_expression(self):
        mul = 1
        if self.scanner.peekChar() == '-':
            self.scanner.shift()
            mul = -mul
        result = self.get_term()
        while self.scanner.peekChar() in ('+', '-'):
            op = self.scanner.peekChar()
            self.scanner.shift()
            if op:
                if op == '+':
                    result += self.get_term()
                elif op == '-':
                    result -= self.get_term()
        return result * mul

    def get_term(self):
        result = self.get_factor()
        while self.scanner.peekChar() in ('*', '/'):
            op = self.scanner.peekChar()
            self.scanner.shift()
            if op:
                if op == '*':
                    result *= self.get_factor()
                elif op == '/':
                    divisor = self.get_factor()
                    if divisor == 0:
                        raise Exception("Division by zero")
                    result //= divisor
        return result

    def get_factor(self):
        if self.scanner.peekChar() == '(':
            self.scanner.shift()
            result = self.get_expression()
            if not self.scanner.getChar(')'):
                raise Exception("Missing closing parenthesis")
        elif self.scanner.testString("RND"):
            result = self.handle_RND()
        elif self.scanner.peekChar().isalpha():
            var_name = self.parser.getVariable()
            result = self.variables.get(var_name)
        elif self.scanner.peekChar().isdigit():
            result = self.scanner.getNumber()
        else:
            raise Exception("Invalid expression")
        return result

    def handle_RND(self):
        self.scanner.shift(len("RND"))
        if not self.scanner.getChar('('):
            raise Exception("Expected '(' after RND")
        max_value = self.get_expression()
        if not self.scanner.getChar(')'):
            raise Exception("Expected ')' after RND argument")
        return random.randint(0, max(max_value - 1, 0))
    
    def get_logical_expression(self):
        """Разбор и вычисление логического выражения."""
        result = self.get_expression()
        while True:
            if self.scanner.testString("AND"):
                self.scanner.shift(len("AND"))
                operand = self.get_expression()
                result = result and operand
            elif self.scanner.testString("OR"):
                self.scanner.shift(len("OR"))
                operand = self.get_expression()
                result = result or operand
            elif self.scanner.testString("NOT"):
                self.scanner.shift(len("NOT"))
                result = not self.get_expression()
            else:
                break
        return result

    def get_comparison(self):
        """Разбор и вычисление сравнений."""
        left = self.get_expression()
        while True:
            if self.scanner.peekChar() in ('<', '>', '='):
                op = self.scanner.peekChar()
                self.scanner.shift()
                if op == '<':
                    if self.scanner.peekChar() == '>':
                        self.scanner.shift()
                        right = self.get_expression()
                        return left != right
                    elif self.scanner.peekChar() == '=':
                        self.scanner.shift()
                        right = self.get_expression()
                        return left <= right
                    else:
                        right = self.get_expression()
                        return left < right
                elif op == '>':
                    if self.scanner.peekChar() == '=':
                        self.scanner.shift()
                        right = self.get_expression()
                        return left >= right
                    else:
                        right = self.get_expression()
                        return left > right
                elif op == '=':
                    right = self.get_expression()
                    return left == right
            else:
                break
        return left