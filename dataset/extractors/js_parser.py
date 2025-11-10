import argparse
import json

import tree_sitter_javascript
from tree_sitter import Language, Parser


def main(file_path):
    code = open(file_path).read()
    parser = Parser()
    parser.language = Language(tree_sitter_javascript.language())
    tree = parser.parse(bytes(code, "utf8"))

    methods = extract_methods(tree.root_node, code.encode("utf8"))

    result = {"methods": methods}
    obj = json.dumps(result, indent=4)
    print(obj)


def extract_methods(node, code):
    methods = []

    # Function declarations like: function foo() { ... }
    if node.type == 'function_declaration':
        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        methods.append((code[node.start_byte:node.end_byte].decode('utf-8'), start_line, end_line))

    # Variable declarators: const foo = () => {}, or const foo = function() {}
    elif node.type == 'variable_declarator':
        value_node = node.child_by_field_name('value')
        if value_node and value_node.type in ('arrow_function', 'function'):
            start_line = value_node.start_point[0] + 1
            end_line = value_node.end_point[0] + 1
            methods.append((code[node.start_byte:node.end_byte].decode('utf-8'), start_line, end_line))

    # Class or object method definitions: greet() { ... }, constructor(...) { ... }
    elif node.type == 'method_definition':
        start_line = node.start_point[0] + 1
        end_line = node.end_point[0] + 1
        methods.append((code[node.start_byte:node.end_byte].decode('utf-8'), start_line, end_line))

    elif node.type == 'pair':
        value_node = node.child_by_field_name('value')
        if value_node and value_node.type == 'function':
            start_line = value_node.start_point[0] + 1
            end_line = value_node.end_point[0] + 1
            methods.append((code[node.start_byte:node.end_byte].decode('utf-8'), start_line, end_line))


    # Recurse into child nodes
    for child in node.children:
        methods.extend(extract_methods(child, code))

    return methods


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract methods from a JS file.')
    parser.add_argument('file_path', type=str, help='Path to the JS file')
    args = parser.parse_args()

    main(args.file_path)
