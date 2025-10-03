# other_statements.py - Parser untuk Jump statements dan lainnya
from lark import Transformer
from parserLogic import ParserLogic

class OtherStatementParser(ParserLogic):
    def __init__(self) -> None:
        super().__init__()

    def start(self, items):
        return items[0]

    def program(self, items):
        return "\n".join([str(item) for item in items if item and str(item).strip()])

    def return_stmt(self, items):
        # return_stmt: KEMBALIKAN expression? ";"?
        if len(items) > 1:
            return f"return {items[1]};"
        return "return;"

    def break_stmt(self, items):
        # break_stmt: BERHENTI ";"?
        return "break;"

    def continue_stmt(self, items):
        # continue_stmt: LANJUT ";"?
        return "continue;"

    def throw_stmt(self, items):
        # throw_stmt: LEMPAR expression ";"?
        return f"throw {items[1]};"

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
