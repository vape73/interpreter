import sys
from interpreter import Interpreter
from source import Source
from variables import Variables
from expressions import Expressions

def main(file_path):
    # Load the program from the file
    source = Source()
    source.load(file_path)

    # Initialize variables and expressions handlers
    variables = Variables()
    expressions = Expressions(variables)

    # Create an instance of the Interpreter
    interpreter = Interpreter(source, variables, expressions)

    # Run the program
    interpreter.run()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python this_script.py <path_to_basic_file>")
    else:
        file_path = sys.argv[1]
        main(file_path)
