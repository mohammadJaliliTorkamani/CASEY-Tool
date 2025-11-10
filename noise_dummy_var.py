import ast
import re

from Java_AST_dummyVar import JavaASTModifierDummyVar


class DummyVarInserter:
    def __init__(self, ext: str):
        self.ext = ext

    def insert_dummy_var(self, methods):
        """
        Insert a dummy variable declaration/assignment like `CaseyVar = 0`
        into each method in `methods` (list of code strings).
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
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code  # fallback if parsing fails

        code_lines = code.splitlines()
        funcs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

        for func in funcs:
            if not func.body:
                continue
            first_stmt_line = func.body[0].lineno - 1
            indent_match = re.match(r'^(\s*)', code_lines[first_stmt_line])
            indent = indent_match.group(1) if indent_match else "    "
            dummy_line = f"{indent}CaseyVar = 0"
            code_lines.insert(first_stmt_line, dummy_line)

        return "\n".join(code_lines)

    # ---------------- PHP ----------------
    def _insert_php(self, code):
        noise_body = "$CaseyVar = 0;"
        m = re.search(r'\bfunction\b', code)
        if not m:
            return code

        brace_pos = code.find('{', m.end())
        if brace_pos == -1:
            # fallback: insert after function signature line
            code_lines = code.split("\n")
            for i, line in enumerate(code_lines):
                if line.strip().startswith("function") or line.strip().startswith("public function"):
                    indent = re.match(r'^\s*', line).group(0) + "    "
                    code_lines.insert(i + 1, indent + noise_body)
                    break
            return "\n".join(code_lines)

        brace_line_start = code.rfind('\n', 0, brace_pos) + 1
        brace_line = code[brace_line_start: code.find('\n', brace_line_start) if code.find('\n',
                                                                                           brace_line_start) != -1 else len(
            code)]

        next_line_start = code.find('\n', brace_pos)
        body_indent = None
        if next_line_start != -1:
            next_line_start += 1
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
        if body_indent is None:
            brace_indent = re.match(r'^\s*', brace_line).group(0)
            body_indent = brace_indent + "    "

        insertion = "\n" + body_indent + noise_body + "\n"
        new_code = code[:brace_pos + 1] + insertion + code[brace_pos + 1:]
        return new_code

    # ---------------- Java ----------------
    def _insert_java(self, code):
        return JavaASTModifierDummyVar().insert_and_return_method(code)

    # ---------------- JS / TS ----------------
    def _insert_js_ts(self, code):
        noise = "let CaseyVar = 0;"
        code_lines = code.split("\n")

        for i, line in enumerate(code_lines):
            stripped = line.strip()
            # Detect function start: normal, async, or arrow
            if (
                    stripped.startswith("function")
                    or stripped.startswith("async function")
                    or "=>" in line
            ):
                # Find line with opening brace {
                for j in range(i, len(code_lines)):
                    if "{" in code_lines[j]:
                        # Determine indentation of next line
                        next_line_indent = "    "
                        if j + 1 < len(code_lines):
                            indent_match = re.match(r'^(\s*)', code_lines[j + 1])
                            if indent_match:
                                next_line_indent = indent_match.group(1)
                        # Insert dummy variable after {
                        code_lines.insert(j + 1, next_line_indent + noise)
                        return "\n".join(code_lines)
                # fallback: insert after function line if no { found
                code_lines.insert(i + 1, "    " + noise)
                return "\n".join(code_lines)
        return code

    # ---------------- C / C++ / Go ----------------
    def _insert_c_cpp_go(self, code):
        if self.ext == ".go":
            noise = "var CaseyVar int = 0"
        else:
            noise = "int CaseyVar = 0;"
        code_lines = code.split("\n")
        for i, line in enumerate(code_lines):
            if "{" in line:
                next_line_indent = "    "
                if i + 1 < len(code_lines):
                    indent_match = re.match(r'^(\s*)', code_lines[i + 1])
                    if indent_match:
                        next_line_indent = indent_match.group(1)
                code_lines.insert(i + 1, next_line_indent + noise)
                break
        return "\n".join(code_lines)

    # ---------------- Ruby ----------------
    def _insert_ruby(self, code):
        noise = "CaseyVar = 0"
        code_lines = code.split("\n")
        for i, line in enumerate(code_lines):
            if line.strip().startswith("def "):
                next_line_indent = "    "
                if i + 1 < len(code_lines):
                    indent_match = re.match(r'^(\s*)', code_lines[i + 1])
                    if indent_match:
                        next_line_indent = indent_match.group(1)
                code_lines.insert(i + 1, next_line_indent + noise)
                break
        return "\n".join(code_lines)
