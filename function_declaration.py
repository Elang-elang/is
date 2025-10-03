# function_declaration.py - Parser untuk Function declarations
from lark import Transformer
from variable_declaration import VariableDeclarationParser

class FunctionDeclarationParser(VariableDeclarationParser):
    def __init__(self) -> None:
        super().__init__()
        self.indent_level = 0
    
    def _get_indent(self):
        return "    " * self.indent_level
    
    def _type_to_ts(self, type_name):
        type_mapping = {
            'teks': 'string',
            'angka': 'number', 
            'kondisi': 'boolean',
            'kosong': 'void',
            'tiada': 'null',
            'tidakTahu': 'unknown',
            'apapun': 'any',
            'objek': 'object',
            'elemen': 'ReactElement',
            'kamus': 'Map',
            'daftar': 'Array',
            'regex': 'RegExp'
        }
        return type_mapping.get(str(type_name), str(type_name))

    def func_decl(self, items):
        # func_decl: func_modifiers? FUNGSI IDENTIFIER "(" params? ")" ":" type_annot statement* BERAKHIR ";"?
        current_index = 0
        modifiers = []
        
        # func_modifiers (opsional)
        if items[0] in ['singkronkan', 'async']:
            modifiers = "singkronkan"
            current_index += 1
        elif items[0] in ['statik', 'static', 'statis']:
            modifiers = "static"
            current_index += 1

        if items[current_index] == "fungsi":
            current_index += 1
        
        # IDENTIFIER (wajib)
        name = str(items[current_index])
        current_index += 1
        
        # params (opsional)
        params = []
        if isinstance(items[current_index], list) or isinstance(items[current_index], str):
            params = items[current_index]
            current_index += 1
        
        # type_annot (wajib)
        return_type = items[current_index]
        current_index += 1
        
        # statement* (sisa items adalah body statements)
        body = items[current_index:-1]
        
        # Generate JavaScript function
        js_modifiers = ""
        if 'singkronkan' in modifiers:
            js_modifiers += "async "
        if 'statis' in modifiers:
            js_modifiers += "static "
        
        # Build parameter list
        param_list = [str(param) for param in params]
        params_str = ", ".join(param_list)
        return_ts_type = self._type_to_ts(return_type)
        
        # Build function body
        self.indent_level += 1
        body_statements = []
        for stmt in body:
            if stmt and str(stmt).strip():
                body_statements.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(body_statements) if body_statements else f"{self._get_indent()}// function body"
        
        return f"{js_modifiers}function {name}({params_str}): {return_ts_type} {{\n{body_str}\n}}"

    def func_modifiers(self, items):
        return items

    def func_modifier(self, items):
        return items[0]

    def params(self, items):
        return items

    def param(self, items):
        # param: IDENTIFIER ":" type_annot param_default?
        param_name = str(items[0])
        param_type = self._type_to_ts(items[1])
        
        default_val = ""
        if len(items) > 2 and hasattr(items[2], 'data') and items[2].data == 'param_default':
            default_val = f" = {items[2].children[0]}"
        
        return f"{param_name}: {param_type}{default_val}"

    def param_default(self, items):
        # param_default: "=" expression
        return items[0]
