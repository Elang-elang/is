# try_statement.py - Parser untuk Try-Catch-Finally statements
from lark import Transformer
from swicth_statement import SwitchStatementParser

class TryStatementParser(SwitchStatementParser):
    def __init__(self) -> None:
        super().__init__()
        self.indent_level = 0
    
    def _get_indent(self):
        return "    " * self.indent_level

    def try_stmt(self, items):
        # try_stmt: COBA MENCOBA statement* try_continuation
        try_body = items[2:-1]  # Skip 'coba', 'mencoba'
        
        self.indent_level += 1
        try_statements = []
        for stmt in try_body:
            if stmt and str(stmt).strip():
                try_statements.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        try_str = "\n".join(try_statements) if try_statements else f"{self._get_indent()}// try body"
        
        result = f"try " + "{" + f"\n{try_str}\n" + f"{items[-1] if (items[-1]) else "}"}"
        
        return result

    def try_continuation(self, items):
        result = ""
        
        # items[0] = 'akhir' -> tutup try block
        result += "}"
        
        # items[1] = 'tangkap', items[2] = identifier, items[3] = 'lakukan'
        catch_var = items[2]
        result += f" catch ({catch_var}) {{"
        
        # Ambil catch statements (skip 'akhir', 'tangkap', identifier, 'lakukan')
        catch_body = items[4:-1]
        
        self.indent_level += 1
        catch_statements = []
        for stmt in catch_body:
            if stmt and str(stmt).strip():
                catch_statements.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        catch_str = "\n".join(catch_statements) if catch_statements else f"{self._get_indent()}// catch body"
        result += f"\n{catch_str}\n"
        
        # Process finally jika ada
        finally_part = items[-1]
        result += finally_part
        
        return result

    def try_finally_or_end(self, items):
        if len(items) == 1 and items[0] == 'berakhir':
            return "}"
        
        # Case 2: Ada finally block
        result = "}"  # Tutup catch block dulu
        
        result += " finally {"
        
        # Parse finally statements
        start_index = 2
        if items[2] == 'lakukan':
            start_index = 3
        elif len(items) > 3 and items[3] == 'lakukan':
            start_index = 4
        
        finally_body = []
        for i in range(start_index, len(items)):
            if items[i] != 'berakhir':
                finally_body.append(items[i])
        
        self.indent_level += 1
        finally_statements = []
        for stmt in finally_body:
            if stmt and str(stmt).strip():
                finally_statements.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        finally_str = "\n".join(finally_statements) if finally_statements else f"{self._get_indent()}// finally body"
        result += f"\n{finally_str}\n}}"
        
        return result
