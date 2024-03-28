class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"{self.type}:{self.value}"