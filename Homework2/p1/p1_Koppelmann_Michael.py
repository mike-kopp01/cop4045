# Question 1
import ast
import io
import os
import tokenize

def line_number(john: str, rachel: str) -> None:

    try: 
        if os.path.abspath(john) == os.path.abspath(rachel):
            raise ValueError("input and outoput name the same file")
        with open(john, encoding="utf-8") as fin, \
                open(rachel, "w", encoding="utf-8") as fout:
            for number, line in enumerate(fin, start=1):
                fout.write(f"{number}. {line.rstrip()}\n")
    except (OSError, ValueError) as err:
        print(f"Error: could not write at all '{rachel}' from '{john}': '{err}'")
        raise

def parse_function(classes: str) -> tuple[tuple[int, str, str, str], ...]:

    try:
        with open(classes, encoding="utf-8") as fin:
            source = fin.read()
        lines = source.splitlines()
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type == tokenize.COMMENT:
                row, col = token.start
                lines[row - 1] = lines[row - 1][:col]
        functions = [
            (node.lineno, node.name, ast.unparse(node.args),
                "".join(line.rstrip() + "\n"
                    for line in lines[node.lineno - 1:node.end_lineno] 
                    if line.strip()))
            for node in ast.walk(ast.parse(source, classes))
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        return tuple(sorted(functions, key=lambda item: item[1]))
    except (OSError, SyntaxError) as err:
        print(f"Error: could not parse at all '{classes}': '{err}'")
        raise
def main() -> None:
    this_file = os.path.abspath(__file__)
    line_number(this_file, this_file + ".txt")
    for function in parse_function(this_file):
        print(function)

if __name__ == "__main__":
    main()
