from line_scanner import LineScanner

class LineParser:
    def __init__(self, scanner: LineScanner):
        self.scanner = scanner

    def getVariable(self):
        """Возвращает имя переменной, если оно находится по текущему указателю."""
        self.scanner.getSpaces()
        var = self.scanner.getChars('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        if var is not None and var.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return var.upper()
        return None

    def getQuotedString(self):
        """Возвращает строку внутри кавычек, пропуская пробелы."""
        self.scanner.getSpaces()
        if self.scanner.peekChar() == '"':
            self.scanner.shift()
            start_pos = self.scanner.pos
            while not self.scanner.isEOL():
                if self.scanner.peekChar() == '"':
                    quoted_string = self.scanner.line[start_pos:self.scanner.pos]
                    self.scanner.shift() 
                    return quoted_string
                self.scanner.shift()
            raise ValueError("Пропущена закрывающая кавычка") 
        return None
