# interpreter.py - Main Transpiler menggunakan Modular Components
from lark import Lark
from grammar import ISMODULAR_GRAMMAR  
from import_export import ImportExportParser as Parsers

class ISModular:
    def __init__(self):
        try:
            self.parser = Lark(ISMODULAR_GRAMMAR, parser='lalr')
            self.transpiler = Parsers()
            print("✓ ISModular Transpiler berhasil diinisialisasi")
        except Exception as e:
            print(f"❌ Error inisialisasi: {e}")
            raise
    
    def transpile(self, code: str) -> str:
        try:
            print("🔍 Parsing kode...")
            tree = self.parser.parse(code)
            
            print("🌳 AST berhasil dibuat")
            
            print("\n🚀 Transpiling ke TypeScript...")
            result = self.transpiler.transform(tree)
            
            print("\n✅ Transpilasi selesai")
            return result
            
        except Exception as e:
            print(f"❌ Error transpilasi: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def run(self, code: str) -> str:
        return self.transpile(code)

if __name__ == '__main__':
    from sys import argv
    if str(argv[0]).endswith('.py'):
        if len(argv) > 1:
            if not str(argv[1]).endswith(".is"):
                raise Exception('error karena file tidak berakhiran \'.is\'')

            isi_file: str = ""
            with open(argv[1], 'r') as f:
                isi_file = str(f.read())

            print(ISModular().transpile(isi_file))
    else:
        raise Exception('error karena file tidak ada, tolong masukan file untuk di Parsing')

