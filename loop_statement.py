# loop_statements.py - Parser untuk Loop statements (for, while, do-while)
from lark import Transformer
from try_statement import TryStatementParser

class LoopStatementParser(TryStatementParser):
    def __init__(self) -> None:
        super().__init__()
        self.indent_level = 0
    
    def _get_indent(self):
        return "    " * self.indent_level
    
    def _modifier_to_js(self, modifier):
        modifier_mapping = {
            'buatkan': 'let',
            'tetapkan': 'const',
            'variabel': 'var'
        }
        return modifier_mapping.get(modifier, 'let')
    
    def _type_to_ts(self, type_name):
        type_mapping = {
            'teks': 'string',
            'angka': 'number', 
            'kondisi': 'boolean',
            'kosong': 'void',
            'tiada': 'null',
            'tidakTahu': 'unknown',
            'apapun': 'any',
            'objek': 'object'
        }
        return type_mapping.get(str(type_name), str(type_name))

    def for_stmt(self, items):
        return items[0]  # Delegate ke specific implementation

    def for_c_style(self, items):
        current_index = 1  # Skip UNTUK
        init_part = ""
        condition_part = ""
        increment_part = ""
        
        # Cari posisi 'lakukan'
        lakukan_index = -1
        for i, item in enumerate(items):
            if str(item) == 'lakukan':
                lakukan_index = i
                break
        
        # Parse bagian for loop
        parts = []
        current_part = []
        
        for i in range(current_index, lakukan_index):
            if str(items[i]) == ';':
                parts.append(current_part)
                current_part = []
            else:
                current_part.append(items[i])
        
        if current_part:
            parts.append(current_part)
        
        # Assign parts
        if len(parts) >= 1 and parts[0]:
            init_part = " ".join([str(p) for p in parts[0]])
        if len(parts) >= 2 and parts[1]:
            condition_part = " ".join([str(p) for p in parts[1]])
        if len(parts) >= 3 and parts[2]:
            increment_part = " ".join([str(p) for p in parts[2]])
        
        # Body statements
        body_statements = []
        for i in range(lakukan_index + 1, len(items)):
            if str(items[i]) != 'berakhir':
                body_statements.append(items[i])
        
        # Generate body
        self.indent_level += 1
        body = []
        for stmt in body_statements:
            if stmt and str(stmt).strip():
                body.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(body) if body else f"{self._get_indent()}// for body"
        
        return f"for ({init_part}; {condition_part}; {increment_part}) {{\n{body_str}\n}}"

    def for_in_style(self, items):
        for_var = items[1]
        iterable = items[3]
        
        # Find 'lakukan' index
        lakukan_index = -1
        for i, item in enumerate(items):
            if str(item) == 'lakukan':
                lakukan_index = i
                break
        
        # Body statements
        body_statements = []
        for i in range(lakukan_index + 1, len(items)):
            if str(items[i]) != 'berakhir':
                body_statements.append(items[i])
        
        # Generate body
        self.indent_level += 1
        body = []
        for stmt in body_statements:
            if stmt and str(stmt).strip():
                body.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(body) if body else f"{self._get_indent()}// for-in body"
        
        return f"for ({for_var} of {iterable}) {{\n{body_str}\n}}"

    def for_init(self, items):
        return items[0]

    def for_var(self, items):
        current_index = 0
        modifier = "let"
        
        # Check for var_modifier
        if str(items[current_index]) in ['variabel', 'buatkan', 'tetapkan']:
            modifier = self._modifier_to_js(items[current_index])
            current_index += 1
        
        var_name = str(items[current_index])
        current_index += 1
        var_type = self._type_to_ts(items[current_index])
        
        return f"{modifier} {var_name}: {var_type}"

    def while_stmt(self, items):
        # while_stmt: SELAMA expression ";"? LAKUKAN statement* BERAKHIR ";"?
        condition = items[1]
        
        # Find 'lakukan' index
        lakukan_index = -1
        for i, item in enumerate(items):
            if str(item) == 'lakukan':
                lakukan_index = i
                break
        
        # Body statements
        body_statements = []
        for i in range(lakukan_index + 1, len(items)):
            if str(items[i]) != 'berakhir':
                body_statements.append(items[i])
        
        self.indent_level += 1
        body = []
        for stmt in body_statements:
            if stmt and str(stmt).strip():
                body.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(body) if body else f"{self._get_indent()}// while body"
        
        return f"while ({condition}) {{\n{body_str}\n}}"

    def do_stmt(self, items):
        # do_stmt: KETIKA expression ";"? LAKUKAN statement* BERAKHIR ";"?
        condition = items[1]
        
        # Find 'lakukan' index
        lakukan_index = -1
        for i, item in enumerate(items):
            if str(item) == 'lakukan':
                lakukan_index = i
                break
        
        # Body statements
        body_statements = []
        for i in range(lakukan_index + 1, len(items)):
            if str(items[i]) != 'berakhir':
                body_statements.append(items[i])
        
        self.indent_level += 1
        body = []
        for stmt in body_statements:
            if stmt and str(stmt).strip():
                body.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(body) if body else f"{self._get_indent()}// do body"
        
        return f"do {{\n{body_str}\n}} while ({condition});"
