from token import Token


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def next_token(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        if self.pos >= len(self.text):
            return Token('EOF')

        current_char = self.text[self.pos]
        
        if current_char.isalpha():
            ident = current_char
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isalnum():
                ident += self.text[self.pos]
                self.pos += 1
            return Token('IDENTIFIER', ident)

        if current_char == '=':
            self.pos += 1
            return Token('ASSIGN', '=')

        if current_char.isdigit():
            num = current_char
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                num += self.text[self.pos]
                self.pos += 1
            return Token('NUMBER', int(num))

        if current_char in '+-*/()':
            self.pos += 1
            return Token('OPERATOR', current_char)

        self.pos += 1
        return Token('UNKNOWN', current_char)