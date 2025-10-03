# import_export.py - Parser untuk Import/Export statements
from lark import Transformer
from type_declaration import TypeDeclarationParser

class ImportExportParser(TypeDeclarationParser):
    def __init__(self) -> None:
        super().__init__()

    def import_stmt(self, items):
        return items[0]

    def import_from(self, items):
        # import_from: DARI STRING IMPORT import_spec ";"?
        # Yang masuk: [STRING] [import_spec]
        module = items[1]  # STRING after DARI
        import_spec = items[3]  # After IMPORT
        
        return f"import {import_spec} from {module};"

    def import_namespace(self, items):
        # import_namespace: IMPORT STRING ";"?
        # Yang masuk: [STRING]
        module = items[1]  # STRING after IMPORT
        return f"import {module};"

    def import_spec(self, items):
        return items[0]

    def import_default(self, items):
        return str(items[0])

    def import_named(self, items):
        # import_named: "{" import_list "}"
        # Yang masuk: [import_list]
        imports = items[0]  # import_list
        return f"{{ {imports} }}"

    def import_all(self, items):
        # import_all: "*" AS IDENTIFIER
        # Yang masuk: [IDENTIFIER] (setelah AS)
        alias = items[1]  # After AS
        return f"* as {alias}"

    def import_mixed(self, items):
        # import_mixed: IDENTIFIER "," "{" import_list "}"
        # Yang masuk: [IDENTIFIER] [import_list]
        default = items[0]
        named = items[2]  # After comma
        return f"{default}, {named}"

    def import_list(self, items):
        return ", ".join([str(item) for item in items])

    def import_item(self, items):
        # import_item: IDENTIFIER import_alias?
        # Yang masuk: [IDENTIFIER] [import_alias?]
        name = str(items[0])
        if len(items) > 1 and hasattr(items[1], 'data') and items[1].data == 'import_alias':
            alias = items[1].children[1]  # After AS
            return f"{name} as {alias}"
        return name

    def import_alias(self, items):
        # import_alias: AS IDENTIFIER
        # Yang masuk: [IDENTIFIER] (setelah AS)
        return items[0]

    def export_stmt(self, items):
        return items[0]

    def export_decl(self, items):
        # export_decl: EXPORT DEFAULT? exportable
        # Yang masuk: [DEFAULT?] [exportable]
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
        # export_named: EXPORT "{" export_list "}" export_from? ";"?
        # Yang masuk: [export_list] [export_from?]
        exports = items[1]  # export_list
        
        from_clause = ""
        if len(items) > 2 and hasattr(items[2], 'data') and items[2].data == 'export_from':
            module = items[2].children[1]  # After DARI
            from_clause = f" from {module}"
        
        return f"export {{ {exports} }}{from_clause};"

    def export_all(self, items):
        # export_all: EXPORT "*" AS IDENTIFIER DARI STRING ";"?
        # Yang masuk: [IDENTIFIER] [STRING] (setelah AS dan DARI)
        alias = items[2]  # After AS
        module = items[4]  # After DARI
        return f"export * as {alias} from {module};"

    def exportable(self, items):
        return items[0]

    def export_from(self, items):
        # export_from: DARI STRING
        # Yang masuk: [STRING] (setelah DARI)
        return items[0]

    def export_list(self, items):
        return ", ".join([str(item) for item in items])

    def export_item(self, items):
        # export_item: IDENTIFIER export_alias?
        # Yang masuk: [IDENTIFIER] [export_alias?]
        name = str(items[0])
        if len(items) > 1 and hasattr(items[1], 'data') and items[1].data == 'export_alias':
            alias = items[1].children[1]  # After AS
            return f"{name} as {alias}"
        return name

    def export_alias(self, items):
        # export_alias: AS IDENTIFIER
        # Yang masuk: [IDENTIFIER] (setelah AS)
        return items[0]
