# if_statement.py - Parser untuk If-Else statements
from lark import Transformer
from other_statements import OtherStatementParser

class IfStatementParser(OtherStatementParser):
    def __init__(self) -> None:
        super().__init__()
        self.indent_level = 0
    
    def _get_indent(self):
        return "    " * self.indent_level

    def if_stmt(self, items):
        # if_stmt: JIKA expression ";"? MAKA statement* if_continuation
        condition = ''
        if items[0] == 'jika':
            condition = items[1]
        
        # statement* adalah items sebelum if_continuation
        then_statements = ''
        if items[3] == 'maka':
            then_statements = items[4:-1]
        elif items[4] == 'maka':
            then_statements = items[5:-1]
        elif items[2] == 'maka':
            then_statements = items[3:-1]
        
        # Build if statement body
        self.indent_level += 1
        then_body = []
        for stmt in then_statements: 
            if stmt and str(stmt).strip():
                then_body.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        then_str = "\n".join(then_body) if then_body else f"{self._get_indent()}// if body"
        k = "{"
        result = f"if ({condition}) {k}\n{then_str}\n{items[-1]}"
        
        return result

    def if_continuation(self, items):
        if len(items) == 0:
            return ""

        if items[0] == 'berakhir':
            return '}'

        if items[-1] == 'berakhir':
            items[-1] = '}'

        index = 0
        starts = ''
        condition = ''
        if items[0] == 'akhir':
            if items[1] == 'selain' and items[2] == 'jika':
                starts = 'else if'
                condition = f" ({items[4]})"
                index += 4
            elif items[1] == 'selain' and items[2] != 'jika':
                starts = 'else'
                condition = ''
                index += 2

        index += 1

        then_statements = items[index:-1]
        self.indent_level += 1
        then_body = []
        for stmt in then_statements:
            if stmt and str(stmt).strip():
                then_body.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1

        then_str = "\n".join(then_body) if then_body else f"{self._get_indent()}// if body"

        k="{"
        k2 = '}'
        return f"{k2} {starts}{condition} {k}\n{then_str}\n{items[-1]}"
