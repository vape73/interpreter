class Arithmetics:
    @staticmethod
    def binary(a, op, b):
        """Выполняет арифметическую операцию над двумя операндами."""
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a // b
        else:
            raise ValueError("Unsupported operation")

    @staticmethod
    def unary(op, a):
        """Выполняет унарную операцию над операндом."""
        if op == '-':
            return -a
        else:
            raise ValueError("Unsupported operation")
        