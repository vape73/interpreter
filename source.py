import os
import time

class Source:
    def __init__(self):
        self.lines = {} 

    def get_first_line_number(self):
        return min(self.lines.keys(), default=None)

    def get_next_line_number(self, current_line_number):
        line_numbers = sorted(self.lines.keys())
        current_index = line_numbers.index(current_line_number)
        if current_index < len(line_numbers) - 1:
            return line_numbers[current_index + 1]
        return None

    def get_line(self, line_number):
        return self.lines.get(line_number, '')

    def add_line(self, line_number, line):
        self.lines[line_number] = line

    def clear(self):
        """Очищает текст программы."""
        self.lines.clear()

    def save(self, filename):
        """Сохраняет текст программы в файл."""
        with open(filename, 'w') as file:
            for line_no in sorted(self.lines):
                file.write(f"{line_no} {self.lines[line_no]}\n")

    def load(self, filename):
        """Загружает текст программы из файла."""
        self.clear()
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    if line.strip():
                        line_no, line_text = line.split(maxsplit=1)
                        self.lines[int(line_no)] = line_text.strip()

    def find(self, label):
        """Проверяет, существует ли метка в программе."""
        return label in self.lines
