# variable_declaration.py - Parser untuk Variable declarations
from lark import Transformer
from loop_statement import  LoopStatementParser

class VariableDeclarationParser(LoopStatementParser):
    def __init__(self) -> None:
        super().__init__()
    
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
            'objek': 'object',
            'elemen': 'ReactElement',
            'kamus': 'Map',
            'daftar': 'Array',
            'regex': 'RegExp'
        }
        return type_mapping.get(str(type_name), str(type_name))

    def var_decl(self, items):
        # var_decl: var_modifier? IDENTIFIER ":" type_annot var_init? ";"?
        # Yang masuk: [var_modifier?] [IDENTIFIER] [type_annot] [var_init?]
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
        return items[0]

    def var_init(self, items):
        # var_init: "=" expression  
        return items[0]  # expression
