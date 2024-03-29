import random
from line_scanner import LineScanner
from variables import Variables


class Expressions:
    def __init__(self, variables: Variables):
        self.variables = variables  # Словарь для хранения переменных и их значений
        self.scanner = None  # LineScanner или аналог для чтения выражений

    def set_scanner(self, scanner: LineScanner):
        self.scanner = scanner

    def get_expression(self):
        """Разбор и вычисление выражения."""
        result = self.get_term()
        while self.scanner.peekChar() in ('+', '-'):
            if self.scanner.getChar('+'):
                result += self.get_term()
            elif self.scanner.getChar('-'):
                result -= self.get_term()
        return result

    def get_unsignedexpr(self):
        """Разбор и вычисление выражения без учета знака."""
        if self.scanner.peekChar() == '+':
            self.scanner.shift()
        elif self.scanner.peekChar() == '-':
            self.scanner.shift()
            return -self.get_term()
        return self.get_term()

    def get_factor(self):
        """Разбор и вычисление фактора (число, переменная, выражение в скобках)."""
        if self.scanner.peekChar().isdigit():
            return int(self.scanner.getNumber())
        elif self.scanner.peekChar().isalpha():
            var_name = self.scanner.getChar()
            return self.variables.get(var_name)
        elif self.scanner.getChar('('):
            value = self.get_expression()
            if not self.scanner.getChar(')'):
                raise Exception("Missing closing parenthesis")
            return value
        else:
            raise Exception("Invalid expression")

    def get_term(self):
        """Разбор и вычисление терма (умножение, деление)."""
        result = self.get_factor()
        while self.scanner.peekChar() in ('*', '/'):
            if self.scanner.getChar('*'):
                result *= self.get_factor()
            elif self.scanner.getChar('/'):
                divisor = self.get_factor()
                if divisor == 0:
                    raise Exception("Division by zero")
                result //= divisor
        return result

    def RND(self):
        """Вычисляет выражение и возвращает случайное число от 0 до этого значения."""
        expression_result = self.get_expression()
        return random.randint(0, max(0, expression_result - 1))