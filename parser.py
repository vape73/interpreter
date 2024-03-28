class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            raise Exception(f"Unexpected token: {self.current_token.type}, expected: {token_type}")

    def factor(self):
        """factor : NUMBER"""
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return token.value
        else:
            raise Exception("Syntax error")

    def expr(self):
        """expr : factor ((PLUS | MINUS) factor)*"""
        result = self.factor()

        while self.current_token.type in ('OPERATOR') and self.current_token.value in '+-':
            op = self.current_token
            if op.value == '+':
                self.eat('OPERATOR')
                result += self.factor()
            elif op.value == '-':
                self.eat('OPERATOR')
                result -= self.factor()

        return result
    
    def statement(self):
        """statement : IDENTIFIER ASSIGN expr"""
        var_name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        var_value = self.expr()
        return (var_name, var_value)

    def program(self):
        """program : statement*"""
        results = {}
        while self.current_token.type != 'EOF':
            var_name, var_value = self.statement()
            results[var_name] = var_value
        return results
