class LineScanner:
    def __init__(self, line):
        self.line = line
        self.pos = 0

    def isBOL(self):
        """Проверяет, находится ли указатель в начале строки."""
        return self.pos == 0

    def isEOL(self):
        """Проверяет, достиг ли указатель конца строки."""
        return self.pos >= len(self.line)

    def peekChar(self):
        """Возвращает текущий символ строки без сдвига указателя."""
        if self.pos < len(self.line):
            return self.line[self.pos]
        else:
            return None  # Или можно выбросить исключение, если требуется строгая обработка ошибок

    def testChar(self, ch):
        """Сравнивает текущий символ с заданным."""
        if self.isEOL():
            return False  # Или возвращаем None, если считаем это исключительной ситуацией
        return self.line[self.pos] == ch

    def testSpace(self):
        """Проверяет, является ли текущий символ пробелом или табуляцией."""
        if self.isEOL():
            return False
        return self.line[self.pos] in (' ', '\t')

    def testCharNot(self, ch):
        """Проверяет, не равен ли текущий символ заданному."""
        if self.isEOL():
            return False  # Или None, смотря как вы хотите обрабатывать выход за пределы
        return self.line[self.pos] != ch

    def testChars(self, chars):
        """Проверяет, содержит ли текущая позиция один из заданных символов."""
        if self.isEOL():
            return False
        return self.line[self.pos] in chars

    def testString(self, string):
        """Проверяет, начинается ли строка с данной подстроки с текущей позиции."""
        return self.line.startswith(string, self.pos)

    def testStrings(self, strings):
        """Проверяет, начинается ли строка с одной из заданных подстрок."""
        for string in strings:
            if self.line.startswith(string, self.pos):
                return True
        return False

    def testNumber(self):
        """Проверяет, является ли текущий символ числом."""
        if self.isEOL():
            return False
        return self.line[self.pos].isdigit()
    
    def shift(self, num=1):
        """Сдвигает указатель на заданное число символов."""
        new_pos = self.pos + num
        if 0 <= new_pos <= len(self.line):
            self.pos = new_pos
            return True
        else:
            self.pos = len(self.line) if num > 0 else 0
            return False

    def getChar(self, ch):
        """Возвращает символ, если он совпадает с текущим, и сдвигает указатель."""
        if not self.isEOL() and self.line[self.pos] == ch:
            self.pos += 1
            return ch
        return None

    def getSpace(self):
        """Возвращает пробел или табуляцию, если они есть, и сдвигает указатель."""
        if self.testSpace():
            char = self.line[self.pos]
            self.pos += 1
            return char
        return None

    def getSpaces(self):
        """Возвращает последовательность пробелов и табуляций, сдвигая указатель."""
        spaces = ''
        while self.testSpace():
            spaces += self.line[self.pos]
            self.pos += 1
        return spaces if spaces else None

    def getChars(self, chars):
        """Возвращает символ из заданного набора и сдвигает указатель."""
        if not self.isEOL() and self.line[self.pos] in chars:
            char = self.line[self.pos]
            self.pos += 1
            return char
        return None

    def getCharNot(self, chars):
        """Возвращает символ, не входящий в заданный набор, и сдвигает указатель."""
        if not self.isEOL() and self.line[self.pos] not in chars:
            char = self.line[self.pos]
            self.pos += 1
            return char
        return None

    def getString(self, string):
        """Возвращает подстроку, если она совпадает с текущей позицией, и сдвигает указатель."""
        if self.line[self.pos:].startswith(string):
            self.pos += len(string)
            return string
        return None

    def getNumber(self):
        """Возвращает число из строки и сдвигает указатель."""
        number = ''
        while not self.isEOL() and self.line[self.pos].isdigit():
            number += self.line[self.pos]
            self.pos += 1
        return int(number) if number else None

    def getStrings(self, strings):
        """Возвращает одну из строк массива при совпадении и сдвигает указатель."""
        for string in strings:
            if self.line[self.pos:].startswith(string):
                self.pos += len(string)
                return string
        return None
