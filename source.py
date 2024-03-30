import os
import time

class Source:
    def __init__(self):
        self.lines = {}  # Словарь для хранения строк с ключами в виде номеров

    def get_first_line_number(self):
        # Возвращает номер первой строки программы
        return min(self.lines.keys(), default=None)

    def get_next_line_number(self, current_line_number):
        # Возвращает номер следующей строки после текущей
        line_numbers = sorted(self.lines.keys())
        current_index = line_numbers.index(current_line_number)
        if current_index < len(line_numbers) - 1:
            # print(line_numbers[current_index + 1], self.lines[line_numbers[current_index + 1]])
            return line_numbers[current_index + 1]
        return None

    def get_line(self, line_number):
        # Возвращает строку по номеру
        return self.lines.get(line_number, '')

    def add_line(self, line_number, line):
        # Добавляет строку в программу
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
                    if line.strip():  # Проверяем, не пустая ли строка
                        line_no, line_text = line.split(maxsplit=1)
                        self.lines[int(line_no)] = line_text.strip()

    def find(self, label):
        """Проверяет, существует ли метка в программе."""
        return label in self.lines
