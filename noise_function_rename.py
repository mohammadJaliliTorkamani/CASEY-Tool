import random
import string

# Tree-sitter grammars
import tree_sitter_c
import tree_sitter_cpp
import tree_sitter_go
import tree_sitter_java
import tree_sitter_javascript
import tree_sitter_php
import tree_sitter_ruby
import tree_sitter_typescript
from tree_sitter import Language, Parser


def random_name(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))


class FunctionRenamer:
    def __init__(self, ext: str):
        self.ext = ext
        self.parser = None

        if ext == ".py":
            self.parser_type = "python"
        else:
            self.parser_type = "tree_sitter"
            self.parser = Parser()
            if ext == ".c":
                self.parser.language = Language(tree_sitter_c.language())
            elif ext == ".cpp":
                self.parser.language = Language(tree_sitter_cpp.language())
            elif ext == ".js":
                self.parser.language = Language(tree_sitter_javascript.language())
            elif ext == ".ts":
                self.parser.language = Language(tree_sitter_typescript.language_typescript())
            elif ext == ".php":
                self.parser.language = Language(tree_sitter_php.language_php())
            elif ext == ".rb":
                self.parser.language = Language(tree_sitter_ruby.language())
            elif ext == ".go":
                self.parser.language = Language(tree_sitter_go.language())
            elif ext == ".java":
                self.parser.language = Language(tree_sitter_java.language())
            else:
                raise ValueError(f"Unsupported language: {ext}")

    def rename_functions(self, code: str) -> str:
        if self.parser_type == "python":
            return self._rename_python(code)
        elif self.ext == ".php":
            return self._rename_php(code)
        elif self.ext == ".js":
            return self._rename_js(code)
        elif self.ext == ".ts":
            return self._rename_ts(code)
        elif self.ext == ".java":
            return self._rename_java(code)
        elif self.ext == ".rb":
            return self._rename_rb(code)
        elif self.ext == ".go":
            return self._rename_go(code)
        elif self.ext == ".c":
            return self._rename_c(code)
        elif self.ext == ".cpp":
            return self._rename_cpp(code)
        else:
            raise ValueError(f"No renaming function for {self.ext}")

    # ----------------- Python -----------------
    def _rename_python(self, code: str) -> str:
        import ast
        tree = ast.parse(code)
        code_chars = list(code)

        class FunctionVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                if isinstance(node.parent, ast.Module):
                    start, end = node.name_start, node.name_end
                    code_chars[start:end] = random_name()
                self.generic_visit(node)

        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
            if isinstance(node, ast.FunctionDef):
                node.name_start = node.col_offset + code.splitlines()[node.lineno - 1].find(node.name)
                node.name_end = node.name_start + len(node.name)

        FunctionVisitor().visit(tree)
        return "".join(code_chars)

    # ----------------- PHP -----------------
    def _rename_php(self, code: str) -> str:
        # Wrap in dummy class for parsing
        dummy_code = f"<?php class Dummy {{ {code} }}"
        tree = self.parser.parse(bytes(dummy_code, "utf8"))
        code_chars = list(dummy_code)

        def traverse(node):
            if node.type in ["method_declaration", "function_definition"]:
                for child in node.children:
                    if child.type == "name":
                        start, end = child.start_byte, child.end_byte
                        code_chars[start:end] = random_name()
                        break
            for child in node.children:
                traverse(child)

        traverse(tree.root_node)

        # Strip the dummy wrapper
        prefix_len = len("<?php class Dummy { ")
        suffix_len = 1  # the closing '}'
        return "".join(code_chars)[prefix_len:-suffix_len]

    # ----------------- JavaScript -----------------
    def _rename_js(self, code: str) -> str:
        tree = self.parser.parse(bytes(code, "utf8"))
        code_chars = list(code)

        def traverse(node):
            if node.type in ["function_declaration", "method_definition"]:
                for child in node.children:
                    if child.type == "identifier":
                        start, end = child.start_byte, child.end_byte
                        code_chars[start:end] = random_name()
                        break
            for child in node.children:
                traverse(child)

        traverse(tree.root_node)
        return "".join(code_chars)

    # ----------------- TypeScript -----------------
    def _rename_ts(self, code: str) -> str:
        return self._rename_js(code)  # Same logic as JS

    # ----------------- Java -----------------
    def _rename_java(self, code: str) -> str:
        tree = self.parser.parse(bytes(code, "utf8"))
        code_chars = list(code)
        renamed = False  # Flag to track if we already renamed a method

        def traverse(node):
            nonlocal renamed
            if renamed:
                return  # Stop once the first method is renamed

            if node.type == "method_declaration":
                for child in node.children:
                    if child.type == "identifier":
                        start, end = child.start_byte, child.end_byte
                        code_chars[start:end] = random_name()
                        renamed = True
                        break

            for child in node.children:
                traverse(child)

        traverse(tree.root_node)
        return "".join(code_chars)

    # ----------------- Ruby -----------------
    def _rename_rb(self, code: str) -> str:
        tree = self.parser.parse(bytes(code, "utf8"))
        code_chars = list(code)

        def traverse(node):
            # Catch instance methods
            if node.type == "method" or node.type == "singleton_method":
                for child in node.children:
                    if child.type == "identifier":
                        start, end = child.start_byte, child.end_byte
                        code_chars[start:end] = random_name()
                        break
            # Recursively traverse children
            for child in node.children:
                traverse(child)

        traverse(tree.root_node)
        return "".join(code_chars)

    # ----------------- Go -----------------
    def _rename_go(self, code: str) -> str:
        tree = self.parser.parse(bytes(code, "utf8"))
        code_chars = list(code)

        def traverse(node):
            if node.type == "function_declaration" or node.type == "method_declaration":
                for child in node.children:
                    if child.type == "identifier" or child.type == "field_identifier":
                        start, end = child.start_byte, child.end_byte
                        code_chars[start:end] = random_name()
                        break
            for child in node.children:
                traverse(child)

        traverse(tree.root_node)
        return "".join(code_chars)

    # ----------------- C -----------------
    def _rename_c(self, code: str) -> str:
        tree = self.parser.parse(bytes(code, "utf8"))
        code_chars = list(code)

        def traverse(node):
            if node.type == "function_definition":
                for child in node.children:
                    if child.type == "identifier":
                        start, end = child.start_byte, child.end_byte
                        code_chars[start:end] = random_name()
                        break
            for child in node.children:
                traverse(child)

        traverse(tree.root_node)
        return "".join(code_chars)

    # ----------------- C++ -----------------
    def _rename_cpp(self, code: str) -> str:
        return self._rename_c(code)  # Same logic as C
