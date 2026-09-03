import ast
from typing import Any, Dict, List


class CodeAnalyzer(ast.NodeVisitor):
    """Analyze Python source code and extract behavioral information."""

    def __init__(self) -> None:
        self.code_units: List[Dict[str, Any]] = []
        self._current_function: Dict[str, Any] | None = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        function_data: Dict[str, Any] = {
            "function": node.name,
            "parameters": [
                arg.arg for arg in node.args.args
            ],
            "conditions": [],
            "loops": [],
            "returns": [],
            "transformations": [],
        }

        previous_function = self._current_function
        self._current_function = function_data

        # Visit everything inside the function.
        for child in node.body:
            self.visit(child)

        self.code_units.append(function_data)

        self._current_function = previous_function

    def visit_If(self, node: ast.If) -> None:
        if self._current_function is not None:
            self._current_function["conditions"].append(
                ast.unparse(node.test)
            )

        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        if self._current_function is not None:
            self._current_function["loops"].append(
                f"for {ast.unparse(node.target)} in {ast.unparse(node.iter)}"
            )

        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        if self._current_function is not None:
            self._current_function["loops"].append(
                f"while {ast.unparse(node.test)}"
            )

        self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> None:
        if self._current_function is not None:
            if node.value is not None:
                self._current_function["returns"].append(
                    ast.unparse(node.value)
                )
            else:
                self._current_function["returns"].append("None")

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if self._current_function is not None:
            self._current_function["transformations"].append(
                ast.unparse(node)
            )

        self.generic_visit(node)


def parse_code(source_code: str) -> List[Dict[str, Any]]:
    """
    Parse Python source code and return analyzed functions.
    """

    if not source_code or not source_code.strip():
        return []

    try:
        tree = ast.parse(source_code)
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python source code: {exc}") from exc

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    return analyzer.code_units