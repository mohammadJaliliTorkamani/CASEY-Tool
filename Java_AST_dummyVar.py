import javalang


class JavaASTModifierDummyVar:
    def __init__(self):
        self.noise_decl = "int CaseyVar = 0;"

    def insert_and_return_method(self, method_code: str) -> str:
        """
        Takes a standalone Java method as input, inserts a dummy variable
        into its body using AST, and returns the modified method only.
        """
        # Wrap the method inside a dummy class (needed for parsing)
        wrapped_code = f"public class CaseyWrapper {{\n{method_code}\n}}"

        # Parse
        tree = javalang.parse.parse(wrapped_code)

        # Extract the first method inside DummyWrapper
        class_decl = tree.types[0]  # ✅ fixed (list, not iterator)
        method = class_decl.methods[0]

        # Insert dummy variable at the beginning of the method body
        if method.body:
            method.body.insert(0, self.noise_decl)

        # Return just the method
        return self._method_to_source(method)

    def _method_to_source(self, method) -> str:
        """
        Pretty-print just a method declaration with body.
        """
        # Method signature
        modifiers = " ".join(method.modifiers) if method.modifiers else "public"
        return_type = method.return_type.name if method.return_type else "void"
        params = ", ".join(
            f"{p.type.name} {p.name}" for p in method.parameters
        )
        header = f"{modifiers} {return_type} {method.name}({params}) " + "{"

        # Method body
        lines = [header]
        for stmt in method.body:
            if isinstance(stmt, str):  # injected dummy var
                lines.append("    " + stmt)
            else:
                lines.append("    " + str(stmt))  # fallback
        lines.append("}")
        return "\n".join(lines)
