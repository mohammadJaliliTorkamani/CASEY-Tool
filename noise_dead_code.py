import ast
import random
import re
import string


def random_name(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))


class DeadCodeInserter:
    def __init__(self, ext: str):
        self.ext = ext

    def insert_dead_code(self, methods):
        """
        Insert dead code like `if false print 0` into each method in `methods`.
        `methods` is a list of code strings.
        Returns a list of modified methods.
        """
        noisy_methods = []

        for code in methods:
            if self.ext == ".py":
                noisy_methods.append(self._insert_python(code))
            elif self.ext == ".php":
                noisy_methods.append(self._insert_php(code))
            elif self.ext == ".java":
                noisy_methods.append(self._insert_java(code))
            elif self.ext in [".js", ".ts"]:
                noisy_methods.append(self._insert_js_ts(code))
            elif self.ext in [".c", ".cpp", ".go"]:
                noisy_methods.append(self._insert_c_cpp_go(code))
            elif self.ext == ".rb":
                noisy_methods.append(self._insert_ruby(code))
            else:
                noisy_methods.append(code)

        return noisy_methods

    # ---------------- Python ----------------
    def _insert_python(self, code: str) -> str:
        tree = ast.parse(code)
        code_lines = code.splitlines()

        # Collect function start lines
        funcs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        for func in funcs:
            line_no = func.body[0].lineno - 1  # first statement line
            indent = len(code_lines[line_no]) - len(code_lines[line_no].lstrip())
            dead_code = " " * indent + "if False:\n" + " " * (indent + 4) + "print(0)"
            code_lines.insert(line_no, dead_code)

        return "\n".join(code_lines)

    # ---------------- PHP ----------------
    def _insert_php(self, code):
        """
        Insert the dead-code block INSIDE the function body (right after the opening brace).
        Handles cases where the brace is on the same line as the signature or on the next line,
        and preserves indentation.
        """
        noise_body = "if (false) { echo 0; }"

        # Find first 'function' occurrence (method or free function).
        m = re.search(r'\bfunction\b', code)
        if not m:
            # fallback: no function keyword found — just insert naive way
            return code

        # Find the first '{' after the function keyword
        brace_pos = code.find('{', m.end())
        if brace_pos == -1:
            # No body brace found; fallback to naive insertion after signature line
            code_lines = code.split("\n")
            for i, line in enumerate(code_lines):
                if line.strip().startswith("public function") or line.strip().startswith("function"):
                    indent = re.match(r'^\s*', line).group(0) + "    "
                    code_lines.insert(i + 1, indent + noise_body)
                    break
            return "\n".join(code_lines)

        # Determine indentation for the inserted noise
        # 1) Find the start of the brace line
        brace_line_start = code.rfind('\n', 0, brace_pos) + 1
        brace_line = code[brace_line_start: code.find('\n', brace_line_start) if code.find('\n',
                                                                                           brace_line_start) != -1 else len(
            code)]

        # 2) Try to use indentation of the next non-empty line after the brace
        next_line_start = code.find('\n', brace_pos)
        body_indent = None
        if next_line_start != -1:
            # Move to the start of the next line content
            next_line_start += 1
            # Scan forward to the first non-empty line (but cap scanning)
            scan_pos = next_line_start
            while scan_pos < len(code):
                next_line_end = code.find('\n', scan_pos)
                if next_line_end == -1:
                    next_line_end = len(code)
                next_line = code[scan_pos:next_line_end]
                if next_line.strip() != "":
                    body_indent = re.match(r'^\s*', next_line).group(0)
                    break
                scan_pos = next_line_end + 1

        # If we couldn't find a meaningful next-line indent, use brace-line indent + 4 spaces
        if body_indent is None:
            brace_indent = re.match(r'^\s*', brace_line).group(0)
            body_indent = brace_indent + "    "

        # Construct insertion string: newline + body_indent + noise + newline (so subsequent code keeps structure)
        insertion = "\n" + body_indent + noise_body + "\n"

        # Insert just after the opening brace
        new_code = code[:brace_pos + 1] + insertion + code[brace_pos + 1:]
        return new_code

    # ---------------- Java ----------------
    def _insert_java(self, code):
        noise = "\n        if(false) { System.out.println(0); }"
        code_lines = code.split("\n")
        for i, line in enumerate(code_lines):
            if "{" in line:
                code_lines.insert(i + 1, noise)
                break
        return "\n".join(code_lines)

    # ---------------- JS / TS ----------------
    def _insert_js_ts(self, code):
        noise = "\n    if(false) { console.log(0); } "
        code_lines = code.split("\n")
        for i, line in enumerate(code_lines):
            if line.strip().startswith("function") or "=>" in line:
                code_lines.insert(i + 1, noise)
                break
        return "\n".join(code_lines)

    # ---------------- C / C++ / Go ----------------
    def _insert_c_cpp_go(self, code):
        if self.ext == ".go":
            noise = "\n    if false { fmt.Println(0) } "
        else:
            noise = "\n    if(0) { printf(\"0\"); } "
        code_lines = code.split("\n")
        for i, line in enumerate(code_lines):
            if "{" in line:
                code_lines.insert(i + 1, noise)
                break
        return "\n".join(code_lines)

    # ---------------- Ruby ----------------
    def _insert_ruby(self, code):
        noise = "\n    if false then puts 0 end"
        code_lines = code.split("\n")
        for i, line in enumerate(code_lines):
            if line.strip().startswith("def "):
                code_lines.insert(i + 1, noise)
                break
        return "\n".join(code_lines)
