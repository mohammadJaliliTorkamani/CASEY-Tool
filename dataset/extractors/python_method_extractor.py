import ast
import json
import sys


def extract_methods(python_file):
    with open(python_file, 'r', encoding='utf-8') as file:
        python_code = file.read()

    methods = []
    try:
        tree = ast.parse(python_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                method_body = ast.get_source_segment(python_code, node)
                start_line = node.lineno
                # The end line is available in Python 3.8+ as node.end_lineno
                end_line = getattr(node, 'end_lineno', None)

                methods.append((method_body, start_line, end_line))


    except Exception as e:
        print(e)
        pass
    return methods


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_methods.py <path_to_python_file>")
        sys.exit(1)

    python_file = sys.argv[1]

    methods = extract_methods(python_file)

    output = {
        "methods": methods
    }

    print(json.dumps(output, indent=4))
