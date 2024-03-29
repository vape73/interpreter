import os

class Source:
    def __init__(self):
        self.lines = []  # Список строк программы
        self.lineIdx = -1  # Индекс текущей строки в списке
        self.lineNo = None  # Номер (метка) текущей строки

    def clear(self):
        """Очищает текст программы."""
        self.lines.clear()
        self.lineIdx = -1
        self.lineNo = None

    def save(self, filename):
        """Сохраняет текст программы в файл."""
        with open(filename, 'w') as file:
            for line in self.lines:
                file.write(f"{line}\n")

    def load(self, filename):
        """Загружает текст программы из файла."""
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                self.lines = file.readlines()
            self.lines = [line.strip() for line in self.lines]  # Убираем переносы строк

    def insert(self, newLine):
        """Добавляет строку в программу с упорядочиванием по номерам меток."""
        lineNo = int(newLine.split()[0])
        for i, line in enumerate(self.lines):
            currentLineNo = int(line.split()[0])
            if currentLineNo == lineNo:
                self.lines[i] = newLine
                return
            elif currentLineNo > lineNo:
                self.lines.insert(i, newLine)
                return
        self.lines.append(newLine)

    def _find(self, label):
        """Находит строку по номеру метки."""
        for idx, line in enumerate(self.lines):
            if line.startswith(f"{label} "):
                self.lineNo = label
                self.lineIdx = idx
                return True
        return False

    def _findNext(self):
        """Находит следующую строку по метке."""
        if self.lineIdx + 1 < len(self.lines):
            nextLine = self.lines[self.lineIdx + 1]
            self.lineNo = int(nextLine.split()[0])
            self.lineIdx += 1
            return True
        return False

    def gotoNext(self):
        """Переходит к следующей строке программы."""
        return self._findNext()
