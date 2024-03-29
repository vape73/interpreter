class Variables:
    def __init__(self):
        self.values = {}

    def set(self, varName, varValue):
        """Сохраняет значение переменной."""
        self.values[varName] = varValue

    def get(self, varName):
        """Возвращает значение переменной. Возвращает ноль, если переменная не определена."""
        return self.values.get(varName, 0)

    def reset(self):
        """Удаляет все переменные."""
        self.values.clear()
        
