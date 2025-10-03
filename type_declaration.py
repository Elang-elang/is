# type_declaration.py - Parser untuk Type declarations
from lark import Transformer
from class_declaration import ClassDeclarationParser

class TypeDeclarationParser(ClassDeclarationParser):
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

    def interface_decl(self, items):
        if len(items) == 4:
            return f"interface {items[1]}{items[2]} {items[3]}"
        return f"interface {items[1]} {items[2]}"

        
    def interface_body(self, items):
        body_then = []
        self.indent_level += 1
        for item in items:
            body_then.append(f"{self._get_indent()}{item}")

        body = ",\n".join(body_then) if body_then else f"{self._get_indent()}// statement interfaces"
        self.indent_level -= 1

        return f"{{\n{body}\n}}"

    def interface_part(self, items):
        if len(items) == 3:
           return f"readonly {items[1]}: {items[2]}"
        return f"{items[0]}: {items[1]}"

    def interface_parts(self, items):
        return items[0]

    def interface_array(self, items):
        body = ", ".join(str(item) for item in items)
        return f"[{body}]"

    def interface_object(self, items):
        self.indent_level += 1
        body = f"{{\n{self._get_indent()*2}{items[0]}: {items[1]}\n{self._get_indent()}}}"
        self.indent_level -= 1

        return body

    def enum_decl(self, items):
        modifier = f"{self._modifier_to_js(items[0])} "
        if modifier == 'let ':
            modifier = ''

        return f"{modifier}{items[1]} {items[2]} {items[3]}"

    def enum_members(self, items):
        body_then = []
        self.indent_level += 1
        for stmt in items:
            body_then.append(f"{self._get_indent()}{stmt}")

        body = ",\n".join(body_then) if body_then else f"{self._get_indent()}// statement enums"
        self.indent_level -= 1

        return f"{{\n{body}\n}}"


    def enum_member(self, items):
        return f"{items[0]} = {items[1]}"

    def type_decl(self, items):
        # items[0] dan items[1] tidak perlu saat ini

        index = 2
        name_type = items[index] # nama dari type alias-nya
        index += 1

        generic_params = ""
        if str(items[index]).startswith("<") and str(items[index]).endswith(">"):
            generic_params = items[index]
            index += 1

        stmt = items[index]

        if generic_params:
            return f"type {name_type}{generic_params} = {stmt};"
        return f"type {name_type} = {stmt};"

    def type_modifier(self, items):
        return items[0]

    def type_definition(self, items):
        return items[0]

    def union_type_def(self, items):
        if len(items) == 1:
            return items[0]
        return " | ".join([str(item) for item in items])

    def intersection_type_def(self, items):
        if len(items) == 1:
            return items[0]
        return " & ".join([str(item) for item in items])

    def simple_type_def(self, items):
        return items[0]

    def object_type_def(self, items):
        # self.indent_level += 1
        # members = []
        # for stmt in items:
        #     if stmt or str(stmt).strip() or str(stmt) != 'berakhir':
        #         members.append(f"{self._get_indent()}{stmt}")
        # self.indent_level -= 1
        
        member_str = items[0] # "\n".join(members) if members else f"{self._get_indent()}// type statement"
        return f"{{\n{member_str}\n}}"

    def type_object_members(self, items):
        self.indent_level += 1
        members = []
        for stmt in items:
            if stmt or str(stmt).strip() or str(stmt) != 'berakhir':
                members.append(f"{self._get_indent()}{stmt};")
        self.indent_level -= 1
        
        member_str = "\n".join(members) if members else f"{self._get_indent()}// type statement"
        return f"{member_str}"

    def type_object_member(self, items):
        readonly = ""
        index = 0
        if items[index] == "hanyaDibaca":
            readonly = "readonly "
            index += 1

        name = items[index]
        index += 1

        option = ""
        if items[index] == "?" or (len(items) >= 3):
            option = "? "
            index += 1

        member = items[index]

        return f"{readonly}{name}{option}: {member}"

    def generic_params(self, items):
        # generic_params: "<[" IDENTIFIER ("," IDENTIFIER)* "]>"
        body = ", ".join(str(item) for item in items)
        return f"<{body}>"
    
    def generic_param(self, items):
        return " ".join([str(item) for item in items])

    def block_enum(self, items):
        # block_enum: statement* BERAKHIR ";"?
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
        return items[0]

    def type_annot(self, items):
        return self._type_to_ts(items[0])

    def union_type(self, items):
        if len(items) == 1:
            return items[0]
        return " | ".join([str(item) for item in items])

    def primary_type(self, items):
        return self._type_to_ts(items[0])

    def basic_type(self, items):
        return self._type_to_ts(str(items[0]))

    def custom_type(self, items):
        return self._type_to_ts(str(items[0]))

    def generic_type(self, items):
        if len(items) == 1:
            return items[0]
        
        if items[0] == "kamus":
            return f"{{[key: {items[1]}]: {items[2]}}}"
        elif items[0] == "daftar":
            items = items[1:]
            result = " | ".join([str(item) for item in items])
            return f"[{result}]"

