from lark import Transformer
from typing import Dict, List, Any

class LexerIS(Transformer):
    def __init__(self) -> None:
        pass

    # Keyword - DIPERBAIKI sesuai grammar

    def VAR(s, i):
        return "variabel"
    def LET(s, i):
        return "buatkan"
    def CONST(s, i):
        return "tetapkan"
    def TIPE(s, i):
        return "tipe"
    def FUNGSI(s, i):
        return "fungsi"
    def CLASS(s, i):
        return "kelas"
    def KONSTRUKTOR(s, i):
        return "konstruktor"  # DIPERBAIKI: dari "constructor" ke "konstruktor"
    def STATIC(s, i):
        return "statis"  # DIPERBAIKI: dari "static" ke "statis"
    def EXTENDS(s, i):
        return "diperluasKe"  # DIPERBAIKI: dari "extends" ke "diperluasKe"
    def ASYNC(s, i):
        return "singkronkan"  # DIPERBAIKI: dari "async" ke "singkronkan"
    def MENUNGGU(s, i):
        return "menunggu"  # DIPERBAIKI: dari "await" ke "menunggu"
    def IMPORT(s, i):
        return "impor"  # DIPERBAIKI: dari "import" ke "impor"
    def EXPORT(s, i):
        return "ekspor"  # DIPERBAIKI: dari "export" ke "ekspor"
    def DARI(s, i):
        return "dari"
    def AS(s, i):
        return "sebagai"  # DIPERBAIKI: dari "as" ke "sebagai"
    def DEFAULT(s, i):
        return "bawaan"  # DIPERBAIKI: dari "default" ke "bawaan"
    def JIKA(s, i):
        return "jika"
    def SELAIN(s, i):
        return "selain"  # DIPERBAIKI: dari "else" ke "selain"
    def UNTUK(s, i):
        return "untuk"
    def SELAMA(s, i):
        return "selama"  # DIPERBAIKI: dari "while" ke "selama"
    def LAKUKAN(s, i):
        return "lakukan"  # DIPERBAIKI: dari "{" ke "lakukan"
    def KETIKA(s, i):
        return "ketika"  # DIPERBAIKI: dari "do" ke "ketika"
    def PILAH(s, i):
        return "pilahkan"  # DIPERBAIKI: dari "switch" ke "pilahkan"
    def KASUS(s, i):
        return "kasus"
    def BAWAAN(s, i):
        return "bawaan"  # DIPERBAIKI: menggunakan "bawaan" langsung
    def BERHENTI(s, i):
        return "berhentikan"  # DIPERBAIKI: dari "break" ke "berhentikan"
    def LANJUT(s, i):
        return "lanjutkan"  # DIPERBAIKI: dari "continue" ke "lanjutkan"
    def KEMBALIKAN(s, i):
        return "kembalikan"  # DIPERBAIKI: dari "return" ke "kembalikan"
    def COBA(s, i):
        return "coba"  # DIPERBAIKI: dari "try" ke "coba"
    def MENCOBA(s, i):
        return "mencoba"  # DIPERBAIKI: dari "{" ke "mencoba"
    def TANGKAP(s, i):
        return "tangkap"  # DIPERBAIKI: dari "catch" ke "tangkap"
    def AKHIRNYA(s, i):
        return "akhirnya"  # DIPERBAIKI: dari "finally" ke "akhirnya"
    def LEMPAR(s, i):
        return "lemparkan"  # DIPERBAIKI: dari "throw" ke "lemparkan"
    def DALAM(s, i):
        return "dalam"  # DIPERBAIKI: dari "of" ke "dalam"
    def MAKA(s, i):
        return "maka"  # DIPERBAIKI: dari "{" ke "maka"
    def AKHIR(s, i):
        return "akhir"  # DIPERBAIKI: dari "}" ke "akhir"
    def BERAKHIR(s, i):
        return "berakhir"  # DIPERBAIKI: dari "}" ke "berakhir"
    def TEKS(s, i):
        return "teks"  # DIPERBAIKI: dari "string" ke "teks"
    def ANGKA(s, i):
        return "angka"  # DIPERBAIKI: dari "number" ke "angka"
    def KONDISI(s, i):
        return "kondisi"  # DIPERBAIKI: dari "boolean" ke "kondisi"
    def KOSONG(s, i):
        return "kosong"  # DIPERBAIKI: dari "void" ke "kosong"
    def TIDAK_TAHU(s, i):
        return "tidakTahu"  # DIPERBAIKI: dari "unknown" ke "tidakTahu"
    def TIADA(s, i):
        return "tiada"  # DIPERBAIKI: dari "null" ke "tiada"
    def APAPUN(s, i):
        return "apapun"  # DIPERBAIKI: dari "any" ke "apapun"
    def ELEMEN(s, i):
        return "elemen"  # DIPERBAIKI: dari "ReactElement" ke "elemen"
    def OBJEK(s, i):
        return "objek"  # DIPERBAIKI: dari "object" ke "objek"
    def KAMUS(s, i):
        return "kamus"  # DIPERBAIKI: dari "kamus" (tetap sama)
    def DAFTAR(s, i):
        return "daftar"  # DIPERBAIKI: dari "daftar" (tetap sama)
    def REGEX(s, i):
        return "regex"  # DIPERBAIKI: dari "regex" (tetap sama)
    def ATAU(s, i):
        return "atau"  # DIPERBAIKI: dari "||" ke "atau"
    def DAN(s, i):
        return "dan"  # DIPERBAIKI: dari "&&" ke "dan"
    def TIDAK(s, i):
        return "tidak"  # DIPERBAIKI: dari "!" ke "tidak"
    def TIPE_DARI(s, i):
        return "tipeDari"  # DIPERBAIKI: dari "typeof" ke "tipeDari"
    def HAPUS(s, i):
        return "hapuskan"  # DIPERBAIKI: dari "delete" ke "hapuskan"
    def INI(s, i):
        return "simpan"  # DIPERBAIKI: dari "simpan" (tetap sama)
    def SIMPANAN(s, i):
        return "simpanan"  # DIPERBAIKI: dari "simpanan" (tetap sama)
    def INDUK(s, i):
        return "masukanInduk"  # DIPERBAIKI: dari "super" ke "masukanInduk"
    def PANGGIL(s, i):
        return "panggil"  # DIPERBAIKI: dari "call" ke "panggil"

    # Configure - DIPERBAIKI

    def ACODING(s, i):
        return "acoding"
    def XML(s, i):
        return "xml"
    def MODULAR(s, i):
        return "modular"
    def SCRIPT(s, i):
        return "script"
    def CONFIG(s, i):
        return "config"

    # Literal - DIPERBAIKI

    def BOOLEAN(s, i):
        return i[0]  # Mengembalikan nilai boolean asli

    def NUMBER(s, i):
        # DIPERBAIKI: Parameter i adalah token, perlu diakses nilai string-nya
        num_str = str(i[0]) if isinstance(i, list) else str(i)
        try:
            if '.' in num_str:
                return float(num_str)
            else:
                return int(num_str)
        except ValueError:
            return float(num_str)

    def STRING(s, i):
        # DIPERBAIKI: Mengembalikan string tanpa mengubah ke template literal
        str_val = i[0] if isinstance(i, list) else i
        return str(str_val)

    def IDENTIFIER(s, i):
        return str(i[0]) if isinstance(i, list) else str(i)
