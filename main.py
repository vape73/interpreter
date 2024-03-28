from lexer import Lexer
from parser import Parser


def interpret(input_text):
    lexer = Lexer(input_text)
    parser = Parser(lexer)
    variables = parser.program()
    return variables

if __name__ == "__main__":
    variables = {}
    while True:
        try:
            text = input("basic> ")
            result = interpret(text)
            variables.update(result)
            for var_name in result:
                print(f"{var_name} = {result[var_name]}")
        except Exception as e:
            print(e)