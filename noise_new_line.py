# noise_new_line.py

import random


class NoiseNewLine:
    """
    Insert random empty lines inside methods while preserving semantics.
    Supports: C, C++, JS, TS, PHP, Ruby, Go, Java, Python.
    """

    def __init__(self, ext):
        self.ext = ext
        pass
        # if ext not in ['.c', '.cpp', '.js', '.ts', '.php', '.rb', '.go', '.java', '.py']:
        #     raise ValueError(f"Unsupported language: {ext}")
        #
        # if ext == '.py':
        #     self.parser_type = 'python'
        # else:
        #     self.parser_type = 'tree_sitter'

    def apply(self, methods):
        """
        methods: list of strings (each is a method)
        returns: list of strings with random empty line inserted
        """
        noisy_methods = []

        for method in methods:
            lines = method.split("\n")
            if len(lines) <= 1:
                # too short, skip insertion
                noisy_methods.append(method)
                continue

            # pick random line inside body (not first or last)
            insert_line = random.randint(1, len(lines) - 1)
            lines.insert(insert_line, "")  # insert empty line

            noisy_methods.append("\n".join(lines))

        return noisy_methods
