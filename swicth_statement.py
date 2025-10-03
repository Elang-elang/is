# switch_statement.py - Parser untuk Switch statements
from lark import Transformer
from if_statement import IfStatementParser

class SwitchStatementParser(IfStatementParser):
    def __init__(self) -> None:
        super().__init__()
        self.indent_level = 0
    
    def _get_indent(self):
        return "    " * self.indent_level

    def switch_stmt(self, items):
        expression = items[1]
        cases = items[3:-1]
        
        self.indent_level += 1
        case_statements = []
        for case in cases:
            case_statements.append(f"{self._get_indent()}{case}\n")
        self.indent_level -= 1
        
        cases_str = "\n".join(case_statements) if case_statements else f"{self._get_indent()}// switch cases"
        
        return f"switch ({expression}) {{\n{cases_str}\n}}"

    def switch_case(self, items):
        return items[0]

    def case_clause(self, items):
        case_value = items[1]  # Skip KASUS
        statements = items[3:-1]
        
        self.indent_level += 1
        case_body = []
        for stmt in statements:
            if stmt:
                case_body.append(f"{self._get_indent()*2}{stmt}")
        
        body_str = "\n".join(case_body) if case_body else f"{self._get_indent()}// case body"
        self.indent_level -= 1

        return f"case {case_value}:\n{body_str}\n{self._get_indent()}"

    def default_clause(self, items):
        statements = items[2:-1]
        
        self.indent_level += 1
        default_body = []
        for stmt in statements:
            if stmt and str(stmt).strip():
                default_body.append(f"{self._get_indent() * 2}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(default_body) if default_body else f"{self._get_indent()}// default body"
        
        return f"default:\n{body_str}\n{self._get_indent()}"
