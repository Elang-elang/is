# class_declaration.py - Parser untuk Class declarations
from lark import Transformer
from function_declaration import FunctionDeclarationParser

class ClassDeclarationParser(FunctionDeclarationParser):
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

    def class_decl(self, items):
        # class_decl: CLASS IDENTIFIER class_extends? class_member* BERAKHIR ";"?
        current_index = 1
        
        # IDENTIFIER (wajib)
        name = str(items[current_index])
        current_index += 1
        
        # class_extends (opsional)
        extends = None
        if current_index < len(items) and "extends" in items[current_index]:
            extends = str(items[current_index])
            current_index += 1
        
        # class_member* (sisa items)
        class_members = []
        for i in range(current_index, len(items) - 1):
            member = items[i]
            if member and str(member).strip():
                class_members.append(f"{self._get_indent()}{member}")
        
        extends_clause = f" {extends}" if extends else ""
        members_str = "\n".join(class_members) if class_members else f"{self._get_indent()}// class members"
        
        return f"class {name}{extends_clause} {{\n{members_str}\n}}"

    def class_extends(self, items):
        # class_extends: EXTENDS IDENTIFIER
        return f"extends {items[1]}"

    def constructor_decl(self, items):
        # constructor_decl: KONSTRUKTOR "(" params? ")" ":" type_annot statement* BERAKHIR ";"?
        current_index = 1
        
        # params (opsional)
        params = items[current_index]
        # if current_index < len(items) and hasattr(items[current_index], 'data') and items[current_index].data == 'params':
        #     params = items[current_index].children
        
        current_index += 1
        
        # type_annot (wajib)
        return_type = items[current_index]
        current_index += 1
        
        # statement* (sisa items)
        body = items[current_index:-1]
        
        # Build parameter list
        param_list = [str(param) for param in params]
        params_str = ", ".join(param_list)
        
        # Build constructor body
        self.indent_level += 2
        body_statements = []
        for stmt in body:
            if stmt and str(stmt).strip():
                body_statements.append(f"{self._get_indent()}{stmt}")
        
        
        body_str = "\n".join(body_statements) if body_statements else f"{self._get_indent()}// constructor body"
        self.indent_level -= 1
        
        result =  f"{self._get_indent()}constructor({params_str}): {return_type} {{\n{body_str}\n{self._get_indent()}}}"
        self.indent_level -= 1
        return result

    def method_decl(self, items):
        # method_decl: method_modifiers? IDENTIFIER "(" params? ")" ":" type_annot statement* BERAKHIR ";"?
        current_index = 0
        modifiers = []
        
        # method_modifiers (opsional)
        if current_index < len(items) and hasattr(items[current_index], 'data') and items[current_index].data == 'method_modifiers':
            modifiers = [str(mod) for mod in items[current_index].children]
            current_index += 1
        
        # IDENTIFIER (wajib)
        name = str(items[current_index])
        current_index += 1
        
        # params (opsional)
        params = []
        if current_index < len(items) and hasattr(items[current_index], 'data') and items[current_index].data == 'params':
            params = items[current_index].children
            current_index += 1
        
        # type_annot (wajib)
        return_type = items[current_index]
        current_index += 1
        
        # statement* (sisa items)
        body = items[current_index:-1]
        
        # Generate method
        js_modifiers = ""
        if 'statis' in modifiers:
            js_modifiers += "static "
        if 'singkronkan' in modifiers:
            js_modifiers += "async "
        
        # Build parameter list
        param_list = [str(param) for param in params]
        params_str = ", ".join(param_list)
        return_ts_type = self._type_to_ts(return_type)
        
        # Build method body
        self.indent_level += 2
        body_statements = []
        for stmt in body:
            if stmt and str(stmt).strip():
                body_statements.append(f"{self._get_indent()}{stmt}")

        
        body_str = "\n".join(body_statements) if body_statements else f"{self._get_indent()}// method body"
        self.indent_level -= 1

        result = f"{self._get_indent()}{js_modifiers}{name}({params_str}): {return_ts_type} {{\n{body_str}\n{self._get_indent()}}}"
        self.indent_level -= 1

        return result

    def method_modifiers(self, items):
        return items
