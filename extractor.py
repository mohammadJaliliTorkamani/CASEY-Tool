import json
import os
import subprocess

import constants


def execute_methods_extractor_python_script(script_name: str, file_name: str):
    command = ['python', script_name, file_name]
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.stdout, process.stderr
    if process.returncode != 0:
        print("Error occurred!", "Stderr:", stderr, "Stdout:", stdout)
        return None

    return json.loads(stdout.encode('utf-8'))['methods']


def parse_method_name(method_code):
    """
    Extract the method/function name from the first line of the method code.
    This is a simple heuristic: get the first line, split on whitespace or parentheses,
    and grab the identifier likely representing the name.
    """
    if not method_code:
        return None

    first_line = method_code.strip().split('\n')[0].strip()
    # Heuristics for different languages (can be improved per language if needed):
    # Examples:
    #   def foo(bar):     -> foo
    #   function foo() {  -> foo
    #   int foo(...) {    -> foo
    #   void foo() {      -> foo
    #   foo() {           -> foo
    #   public void foo() -> foo

    # Try to split by spaces and parentheses to find the name token
    tokens = first_line.replace('(', ' ').replace(')', ' ').replace(':', ' ').split()
    # Reverse tokens to try and find plausible function name (avoid keywords)
    for token in tokens[::-1]:
        if token.isidentifier() and token.lower() not in (
                'def', 'function', 'public', 'private', 'protected', 'static', 'void', 'int', 'char', 'float', 'double',
                'bool',
                'async', 'export', 'const', 'let', 'var'):
            return token
    # fallback
    return tokens[0] if tokens else None


def extract_python_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.PYTHON_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


def extract_java_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.JAVA_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


def extract_js_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.JS_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


def extract_php_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.PHP_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


def extract_ts_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.TS_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


def extract_c_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.C_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


def extract_cpp_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.CPP_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


def extract_go_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.GO_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


def extract_ruby_methods(file_name):
    methods = execute_methods_extractor_python_script(constants.RB_EXTRACTOR_SCRIPT_PATH, file_name)
    if methods is None:
        return []
    return methods


class Extractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_methods(self):
        if not os.path.exists(self.file_path):
            return []
        file_extension = self.file_path.split('/')[-1].split('.')[-1].lower()

        if file_extension == 'php':
            return extract_php_methods(self.file_path)
        elif file_extension == 'js':
            return extract_js_methods(self.file_path)
        elif file_extension == 'go':
            return extract_go_methods(self.file_path)
        elif file_extension == 'ts':
            return extract_ts_methods(self.file_path)
        elif file_extension == 'py':
            return extract_python_methods(self.file_path)
        elif file_extension == 'c':
            return extract_c_methods(self.file_path)
        elif file_extension == 'cpp':
            return extract_cpp_methods(self.file_path)
        elif file_extension == 'rb':
            return extract_ruby_methods(self.file_path)
        elif file_extension == 'java':
            return extract_java_methods(self.file_path)
