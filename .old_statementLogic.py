# statementLogic.py - Statement Logic yang Diperbaiki
from lark import Transformer
from parserLogic import ParserLogic
from typing import Dict, List, Any

class StatementLogic(ParserLogic):
    def __init__(self) -> None:
        super().__init__()
        self.indent_level = 0
    
    def _get_indent(self):
        return "    " * self.indent_level
    
    def _type_to_ts(self, type_name):
        """Convert ISModular types to TypeScript types"""
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
    
    def _modifier_to_js(self, modifier):
        """Convert ISModular variable modifiers to JavaScript"""
        modifier_mapping = {
            'buatkan': 'let',
            'tetapkan': 'const',
            'variabel': 'var'
        }
        return modifier_mapping.get(modifier, 'let')

    def _filters_(self, items: List[Any]) -> List[Any]:
        objects = ['maka', 'lakukan', 'akhir', 'berakhir']
        result_items = []
        for obj in objects:
            for item in items:
                if (obj == item):
                    continue

                result_items.append(item)

        return result_items
    # ================================================
    #             PROGRAM STRUCTURE
    # ================================================
    
    def start(self, items):
        return items[0]

    def program(self, items):
        return "\n".join([str(item) for item in items if item and str(item).strip()])

    # ================================================
    #             VARIABLE DECLARATIONS
    # ================================================
    
    def var_decl(self, items):
        # var_decl: var_modifier? IDENTIFIER ":" type_annot var_init? ";"?
        # Yang masuk: [var_modifier?] [IDENTIFIER] [type_annot] [var_init?]
        # ":" dan ";" tidak masuk karena literal string
        # print(items)
        var_modifier = 'buatkan'
        identifier = None
        type_annot = None
        value = None
        
        current_index = 0
        
        # Cek var_modifier (opsional)
        if items[0] in ['variabel', 'buatkan', 'tetapkan']:
            var_modifier = str(items[0])
            current_index += 1
        
        # IDENTIFIER (wajib ada)
        identifier = str(items[current_index])
        current_index += 1
        
        # type_annot (wajib ada)
        type_annot = items[current_index]
        current_index += 1
        
        # var_init (opsional)
        if len(items) >= 4:
            value = items[3]
            current_index += 1
        
        # Generate JavaScript/TypeScript code
        js_modifier = self._modifier_to_js(var_modifier)
        ts_type = self._type_to_ts(type_annot)
        
        if value is None:
            return f"{js_modifier} {identifier}: {ts_type};"
        else:
            return f"{js_modifier} {identifier}: {ts_type} = {value};"

    def var_modifier(self, items):
        # var_modifier: VAR | LET | CONST
        return items[0]

    def var_init(self, items):
        # var_init: "=" expression  
        # "=" tidak masuk array, hanya expression yang masuk
        return items[0]  # expression

    # ================================================
    #             TYPE DECLARATIONS
    # ================================================
    
    def type_decl(self, items):
        # type_decl: type_modifier TIPE IDENTIFIER generic_params? type_body
        # Yang masuk: [type_modifier] [IDENTIFIER] [generic_params?] [type_body]
        # TIPE tidak masuk karena terminal

        current_index = 0
        
        type_modifier = items[current_index]
        current_index += 1
        
        # Skip TIPE (terminal tidak masuk array)
        identifier = str(items[current_index])
        current_index += 1
        
        generic_params = ""
        if current_index < len(items) and hasattr(items[current_index], 'data') and items[current_index].data == 'generic_params':
            generics = items[current_index].children
            generic_params = f"<{', '.join([str(g) for g in generics])}>"
            current_index += 1
        
        type_body = ""
        if current_index < len(items):
            body = items[current_index]
            if hasattr(body, 'data'):
                if body.data == 'type_alias':
                    type_body = f" = {body}"
                elif body.data == 'block_enum':
                    type_body = f" {body}"
        
        return f"type {identifier}{generic_params}{type_body};"

    def type_modifier(self, items):
        return items[0]

    def generic_params(self, items):
        # generic_params: "<[" IDENTIFIER ("," IDENTIFIER)* "]>"
        # Literal string tidak masuk, hanya IDENTIFIER yang masuk
        return items

    def type_body(self, items):
        return items[0]

    def block_enum(self, items):
        # block_enum: statement* BERAKHIR ";"?
        # Yang masuk: [statement*] (BERAKHIR dan ";" tidak masuk)
        self.indent_level += 1
        members = []
        for stmt in items:
            if stmt and str(stmt).strip() and str(stmt) != 'berakhir':
                members.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        member_str = "\n".join(members) if members else f"{self._get_indent()}// enum members"
        return f"{{\n{member_str}\n}}"

    def type_alias(self, items):
        # type_alias: "=" type_annot
        # "=" tidak masuk, hanya type_annot
        return items[0]

    # ================================================
    #             FUNCTION DECLARATIONS
    # ================================================
    
    def func_decl(self, items):
        # func_decl: func_modifiers? FUNGSI IDENTIFIER "(" params? ")" ":" type_annot statement* BERAKHIR ";"?
        # Yang masuk: [func_modifiers?] [IDENTIFIER] [params?] [type_annot] [statement*]
        # FUNGSI, "(", ")", ":", BERAKHIR, ";" tidak masuk
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
        body = items[current_index:]
        
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
            elif stmt and str(stmt).strip() in ["BERAKHIR", "berakhir"]:
                pass
        self.indent_level -= 1
        
        body_str = "\n".join(body_statements) if body_statements else f"{self._get_indent()}// function body"
        
        return f"{js_modifiers}function {name}({params_str}): {return_ts_type} {{\n{body_str}\n}}"

    def func_modifiers(self, items):
        return items

    def func_modifier(self, items):
        return items[0]

    def iarams(self, items):
        return items

    def param(self, items):
        # param: IDENTIFIER ":" type_annot param_default?
        # Yang masuk: [IDENTIFIER] [type_annot] [param_default?]
        
        param_name = str(items[0])
        param_type = self._type_to_ts(items[1])
        
        default_val = ""
        if len(items) > 2 and hasattr(items[2], 'data') and items[2].data == 'param_default':
            default_val = f" = {items[2].children[0]}"  # expression dari param_default
        
        return f"{param_name}: {param_type}{default_val}"

    def param_default(self, items):
        # param_default: "=" expression
        # "=" tidak masuk, hanya expression
        return items[0]

    # ================================================
    #             CLASS DECLARATIONS
    # ================================================
    
    def class_decl(self, items):
        # class_decl: CLASS IDENTIFIER class_extends? class_member* BERAKHIR ";"?
        # Yang masuk: [IDENTIFIER] [class_extends?] [class_member*]
        
        current_index = 0
        
        # IDENTIFIER (wajib)
        name = str(items[current_index])
        current_index += 1
        
        # class_extends (opsional)
        extends = None
        if current_index < len(items) and hasattr(items[current_index], 'data') and items[current_index].data == 'class_extends':
            extends = str(items[current_index].children[0])  # IDENTIFIER dari EXTENDS IDENTIFIER
            current_index += 1
        
        # class_member* (sisa items)
        class_members = []
        for i in range(current_index, len(items)):
            member = items[i]
            if member and str(member).strip():
                class_members.append(f"{self._get_indent()}{member}")
        
        extends_clause = f" extends {extends}" if extends else ""
        members_str = "\n".join(class_members) if class_members else f"{self._get_indent()}// class members"
        
        return f"class {name}{extends_clause} {{\n{members_str}\n}}"

    def class_extends(self, items):
        # class_extends: EXTENDS IDENTIFIER
        # EXTENDS tidak masuk, hanya IDENTIFIER
        return items[0]

    def constructor_decl(self, items):
        # constructor_decl: KONSTRUKTOR "(" params? ")" ":" type_annot statement* BERAKHIR ";"?
        # Yang masuk: [params?] [type_annot] [statement*]
        
        current_index = 0
        
        # params (opsional)
        params = []
        if current_index < len(items) and hasattr(items[current_index], 'data') and items[current_index].data == 'params':
            params = items[current_index].children
            current_index += 1
        
        # type_annot (wajib)
        return_type = items[current_index]
        current_index += 1
        
        # statement* (sisa items)
        body = items[current_index:]
        
        # Build parameter list
        param_list = [str(param) for param in params]
        params_str = ", ".join(param_list)
        
        # Build constructor body
        self.indent_level += 1
        body_statements = []
        for stmt in body:
            if stmt and str(stmt).strip():
                body_statements.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(body_statements) if body_statements else f"{self._get_indent()}// constructor body"
        
        return f"constructor({params_str}) {{\n{body_str}\n{self._get_indent()}}}"

    def method_decl(self, items):
        # method_decl: method_modifiers? IDENTIFIER "(" params? ")" ":" type_annot statement* BERAKHIR ";"?
        # Yang masuk: [method_modifiers?] [IDENTIFIER] [params?] [type_annot] [statement*]
        
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
        body = items[current_index:]
        
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
        self.indent_level += 1
        body_statements = []
        for stmt in body:
            if stmt and str(stmt).strip():
                body_statements.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(body_statements) if body_statements else f"{self._get_indent()}// method body"
        
        return f"{js_modifiers}{name}({params_str}): {return_ts_type} {{\n{body_str}\n{self._get_indent()}}}"

    def method_modifiers(self, items):
        return items

    # ================================================
    #             CONTROL FLOW STATEMENTS
    # ================================================
    
    def if_stmt(self, items):
        # print(f"{items=}")
        # if_stmt: JIKA expression ";"? MAKA statement* if_continuation
        # Yang masuk: [expression] [statement*] [if_continuation]
        # print(f"{items[-1]=}")
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
        # Berbagai kemungkinan if_continuation berdasarkan grammar
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
                # items[4] skip, => maka
                starts = 'else if'
                condition = f" ({items[4]})"
                index += 4
            elif items[1] == 'selain' and items[2] != 'jika':
                # print(f"{items=}")
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

    # ================================================
    #             JUMP STATEMENTS
    # ================================================
    
    def return_stmt(self, items):
        # return_stmt: KEMBALIKAN expression? ";"?
        # Yang masuk: [expression?]
        
        if len(items) > 0:
            return f"return {items[1]};"
        return "return;"

    def break_stmt(self, items):
        # break_stmt: BERHENTI ";"?
        # Yang masuk: [] (kosong karena semua literal)
        return "break;"

    def continue_stmt(self, items):
        # continue_stmt: LANJUT ";"?
        # Yang masuk: [] (kosong)
        return "continue;"

    def throw_stmt(self, items):
        # throw_stmt: LEMPAR expression ";"?
        # Yang masuk: [expression]
        return f"throw {items[:1]};"

    # ================================================
    #             TYPE ANNOTATIONS
    # ================================================
    
    def type_annot(self, items):
        return self._type_to_ts(items[0])

    def union_type(self, items):
        if len(items) == 1:
            return items[0]
        return " | ".join([str(item) for item in items])

    def primary_type(self, items):
        return items[0]

    def basic_type(self, items):
        return str(items[0])

    def custom_type(self, items):
        return str(items[0])

    def generic_type(self, items):
        return items[0]  # Handle specific generic types

    def func_type(self, items):
        params = ""
        return_type = items[-1]  # Last item is return type
        
        if len(items) > 1 and hasattr(items[0], 'data') and items[0].data == 'func_type_params':
            param_types = items[0].children
            params = ", ".join([self._type_to_ts(param) for param in param_types])
        
        return f"({params}) => {self._type_to_ts(return_type)}"

    def func_type_params(self, items):
        return items

    def array_type(self, items):
        base_type = self._type_to_ts(items[0])
        return f"{base_type}[]"

    def paren_type(self, items):
        return f"({self._type_to_ts(items[0])})"

    # ================================================
    #             TRY-CATCH STATEMENTS
    # ================================================
    
    def try_stmt(self, items):
        # try_stmt: COBA MENCOBA statement* try_continuation
        # Yang masuk: ['coba', 'mencoba', ...statements..., Tree('try_continuation', ...)]
        
        try_body = []
        
        # Ambil statements sebelum try_continuation (skip 'coba', 'mencoba')
        try_body = items[2:-1]  # Jika tidak ada continuation
        
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
        # try_continuation: AKHIR TANGKAP IDENTIFIER LAKUKAN statement* try_finally_or_end
        # Yang masuk: ['akhir', 'tangkap', 'error', 'lakukan', ...statements..., Tree('try_finally_or_end', ...)]
        
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
        # Dua kemungkinan:
        # 1. try_finally_or_end: BERAKHIR ";"? -> hanya ['berakhir']
        # 2. try_finally_or_end: AKHIR AKHIRNYA ";"? LAKUKAN statement* BERAKHIR ";"? 
        #    -> ['akhir', 'akhirnya', 'lakukan', ...statements..., 'berakhir']
        
        if len(items) == 1 and items[0] == 'berakhir':
            # Case 1: Hanya berakhir, tutup catch block
            return "}"
        
        # Case 2: Ada finally block
        result = "}"  # Tutup catch block dulu
        
        # items[0] = 'akhir', items[1] = 'akhirnya', items[2] = 'lakukan' (opsional ';')
        result += " finally {"
        
        # Ambil finally statements (skip 'akhir', 'akhirnya', kemungkinan ';', 'lakukan')
        start_index = 2
        if items[2] == 'lakukan':
            start_index = 3
        elif len(items) > 3 and items[3] == 'lakukan':
            start_index = 4
        
        # Statements adalah dari start_index sampai sebelum 'berakhir'
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

    # ================================================
    #             SWITCH STATEMENTS
    # ================================================
    
    def switch_stmt(self, items):
        # print(f"{items=}")
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
        # print(f"{items=}")
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

    # ================================================
    #             STATEMENT LOOPS
    # ================================================

    def for_stmt(self, items):
        items = items[0]
        print(f"{items=}")
        print(f"{len(items)=}")
        print(
            f"{items in ['lakukan']}\n{["lakukan"] in items}\n{items.index("lakukan")}"
        )
        index = 0

        if 'lakukan' in items:
            try:
                index = items.index('lakukan')
            except Exception:
                for i, ind in enumerate(items):
                    print(f"{ind=}")
        
        statement = items[index:-1]

        condition = "".join(items[1:index])

        body = []
        self.indent_level += 1
        for stmt in statement:
            if stmt:
                body.append(f"{self._get_indent()}{stmt}")

        result_stmt = "\n".join(body) if (body) else f"{self._get_indent()}// for loop statement"
        self.indent_level -= 1

        return f"for ({condition})\n{{{result_stmt}}}"



    def for_in_style(self, items):
        return items

    # ================================================
    #             ARROW FUNCTIONS
    # ================================================
    
    def arrow_func(self, items):
        params = []
        return_type = None
        body = []
        
        i = 1  # Skip '('
        if i < len(items) and hasattr(items[i], 'data') and items[i].data == 'params':
            params = items[i].children
            i += 1
        
        i += 1  # Skip ')'
        
        if i < len(items) and hasattr(items[i], 'data') and items[i].data == 'arrow_return':
            return_type = items[i].children[1]  # Skip ':'
            i += 1
        
        i += 1  # Skip MAKA
        
        # Collect body statements
        while i < len(items) and str(items[i]) != 'berakhir':
            body.append(items[i])
            i += 1
        
        # Build parameter list
        param_list = [str(param) for param in params]
        params_str = ", ".join(param_list)
        
        return_annotation = f": {self._type_to_ts(return_type)}" if return_type else ""
        
        # Build arrow function body
        self.indent_level += 1
        body_statements = []
        for stmt in body:
            if stmt and str(stmt).strip():
                body_statements.append(f"{self._get_indent()}{stmt}")
        self.indent_level -= 1
        
        body_str = "\n".join(body_statements) if body_statements else f"{self._get_indent()}// arrow function body"
        
        return f"({params_str}){return_annotation} => {{\n{body_str}\n}}"

    def arrow_return(self, items):
        return items

    # ================================================
    #             IMPORT/EXPORT STATEMENTS  
    # ================================================
    
    def import_stmt(self, items):
        return items[0]

    def import_from(self, items):
        module = items[1]  # STRING after DARI
        import_spec = items[3]  # After IMPORT
        
        return f"import {import_spec} from {module};"

    def import_namespace(self, items):
        module = items[1]  # STRING after IMPORT
        return f"import {module};"

    def import_spec(self, items):
        return items[0]

    def import_default(self, items):
        return str(items[0])

    def import_named(self, items):
        # print(f"{items=}")
        imports = items[0]  # import_list
        return f"{{ {imports} }}"

    def import_all(self, items):
        # print(f'{items=}')
        alias = items[1]  # After AS
        return f"* as {alias}"

    def import_mixed(self, items):
        default = items[0]
        named = items[2]  # After comma
        return f"{default}, {named}"

    def import_list(self, items):
        return ", ".join([str(item) for item in items])

    def import_item(self, items):
        # print(f"{items=}")
        name = str(items[0])
        if len(items) > 1 and hasattr(items[1], 'data') and items[1].data == 'import_alias':
            alias = items[1].children[1]  # After AS
            return f"{name} as {alias}"
        return name

    def export_stmt(self, items):
        return items[0]

    def export_decl(self, items):
        is_default = False
        exportable = None
        
        i = 1  # Skip EXPORT
        if i < len(items) and str(items[i]) == 'bawaan':
            is_default = True
            i += 1
        
        exportable = items[i]
        
        if is_default:
            return f"export default {exportable}"
        else:
            return f"export {exportable}"

    def export_named(self, items):
        exports = items[1]  # export_list
        
        from_clause = ""
        if len(items) > 2 and hasattr(items[2], 'data') and items[2].data == 'export_from':
            module = items[2].children[1]  # After DARI
            from_clause = f" from {module}"
        
        return f"export {{ {exports} }}{from_clause};"

    def export_all(self, items):
        alias = items[2]  # After AS
        module = items[4]  # After DARI
        return f"export * as {alias} from {module};"

    def exportable(self, items):
        return items[0]

    def export_list(self, items):
        return ", ".join([str(item) for item in items])

    def export_item(self, items):
        name = str(items[0])
        if len(items) > 1 and hasattr(items[1], 'data') and items[1].data == 'export_alias':
            alias = items[1].children[1]  # After AS
            return f"{name} as {alias}"
        return name

    # ================================================
    #             ACODING STATEMENTS
    # ================================================
    
    def acoding_stmt(self, items):
        acoding_type = items[2]  # After "#" and "acoding:"
        
        # Generate appropriate comment or directive based on acoding type
        if str(acoding_type) == 'xml':
            return "// @acoding: xml"
        elif str(acoding_type) == 'modular':
            return "// @acoding: modular"
        elif str(acoding_type) == 'script':
            return "// @acoding: script"
        elif str(acoding_type) == 'config':
            return "// @acoding: config"
        
        return f"// @acoding: {acoding_type}"

    def acoding_type(self, items):
        return items[0]
