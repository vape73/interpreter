from line_scanner import LineScanner

class LineParser:
    def __init__(self, scanner: LineScanner):
        self.scanner = scanner

    def getVariable(self):
        """Возвращает имя переменной, если оно находится по текущему указателю."""
        self.scanner.getSpaces()  # Пропустим пробелы
        var = self.scanner.getChars('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        if var is not None and var.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return var.upper()  # Имена переменных нечувствительны к регистру
        return None

    def getQuotedString(self):
        """Возвращает строку внутри кавычек, пропуская пробелы."""
        self.scanner.getSpaces()  # Пропустим пробелы
        if self.scanner.peekChar() == '"':
            self.scanner.shift()  # Пропускаем открывающую кавычку
            start_pos = self.scanner.pos
            while not self.scanner.isEOL():
                if self.scanner.peekChar() == '"':
                    quoted_string = self.scanner.line[start_pos:self.scanner.pos]
                    self.scanner.shift()  # Пропускаем закрывающую кавычку
                    return quoted_string
                self.scanner.shift()
            raise ValueError("Missing closing quote")  # Если закрывающая кавычка не найдена
        return None
