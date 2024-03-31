import sys
from interpreter import Interpreter
from source import Source
from variables import Variables
from expressions import Expressions

def interactive_mode():
    source = Source()
    variables = Variables()
    expressions = Expressions(variables)
    interpreter = Interpreter(source, variables, expressions)

    print("Вход в интерактивный режим BASIC. Для выхода введите 'EXIT'.")

    while True:
        try:
            line_input = input("> ").strip()
            if line_input.upper() == "EXIT":
                print("Выход из интерактивного режима.")
                break
            
            if line_input.upper().startswith("LOAD "):
                source.clear()
                _, filename = line_input.split(maxsplit=1)
                interpreter.LOAD(filename)
            elif line_input.upper().startswith("SAVE "):
                _, filename = line_input.split(maxsplit=1)
                interpreter.SAVE(filename)
            else:
                l_space = line_input.find(' ')
                num = int(line_input[0:l_space])
                line = line_input[l_space+1:]
                source.add_line(num, line)
                if line.startswith(('GOTO', 'GOSUB')):
                    interpreter.run(num)
                else:
                    interpreter.execute_line(line)

        except Exception as e:
            print(f"Ошибка: {e}")


def file_mode(file_path):
    source = Source()
    source.load(file_path)

    variables = Variables()
    expressions = Expressions(variables)

    interpreter = Interpreter(source, variables, expressions)

    interpreter.run()
if __name__ == "__main__":
    if len(sys.argv) < 2:
        interactive_mode()
    else:
        file_path = sys.argv[1]
        file_mode(file_path)
