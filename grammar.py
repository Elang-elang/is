# grammar.py - Grammar yang diperbaiki sesuai spesifikasi

ISMODULAR_GRAMMAR = r"""
start: program

program: statement*

?statement: var_decl
          | type_decl
          | interface_decl
          | enum_decl
          | func_decl
          | class_decl
          | import_stmt
          | export_stmt
          | if_stmt
          | try_stmt
          | switch_stmt
          | while_stmt
          | do_stmt
          | for_stmt
          | return_stmt
          | break_stmt
          | continue_stmt
          | throw_stmt
          | expr_stmt
          | acoding_stmt

// Variable declaration
var_decl: var_modifier? IDENTIFIER ":" type_annot var_init? ";"?
var_modifier: VAR | LET | CONST
var_init: "=" expression


// Type, Interface, dan Enum declarations - DIPERBAIKI
// Type Declaration - DIPERBAIKI untuk mendukung semua pola TypeScript
type_decl: type_modifier TIPE IDENTIFIER generic_params? "=" type_definition ";"?

type_definition: union_type_def | intersection_type_def | simple_type_def

// Union types: string | number | "literal"
union_type_def: intersection_type_def ("|" intersection_type_def)+

// Intersection types: string & { property: type }
intersection_type_def: simple_type_def ("&" simple_type_def)+

// Simple type definitions
simple_type_def: object_type_def
               | array_type_def
               | tuple_type_def
               | literal_type_def
               | function_type_def
               | generic_instantiation
               | basic_type
               | IDENTIFIER

// Object type: { name: string; age: number }
object_type_def: "{" type_object_members? "}"
type_object_members: type_object_member (";" type_object_member)* ";"?
type_object_member: HANYA_DIBACA? IDENTIFIER optional_marker? ":" type_definition
optional_marker: "?"

// Array types: daftar[string] or string[] or (string | number)[]
array_type_def: DAFTAR "[" type_definition "]"
              | simple_type_def "[" "]"

// Tuple types: [string, number, boolean]
tuple_type_def: "[" type_definition ("," type_definition)* "]"

// Literal types: "literal" | 123 | true
literal_type_def: STRING | NUMBER | BOOLEAN

// Function types: (a: string, b: number) => boolean
function_type_def: "(" params? ")" "=>" type_definition

// Generic instantiation: kamus[string, number]
generic_instantiation: KAMUS "[" type_definition "," type_definition "]"
                     | IDENTIFIER "[" type_definition ("," type_definition)* "]"
                     | IDENTIFIER "<[" type_definition ("," type_definition)* "]>"

// Reusable func_type_params untuk function types

interface_decl: ANTARMUKA IDENTIFIER generic_params? "{" interface_body* "}" ";"?
interface_body: interface_part ("," interface_part)*
interface_part: HANYA_DIBACA? IDENTIFIER ":" interface_parts
interface_parts: interface_array | interface_object | type_annot
interface_array: "[" interface_parts ("," interface_parts)* "]"
interface_object: "{" IDENTIFIER ":" interface_parts "}" 

enum_decl: type_modifier ENUM IDENTIFIER "{" enum_members? "}" ";"?
enum_members: enum_member ("," enum_member)* ","?
enum_member: IDENTIFIER "=" expression

type_modifier: CONST | LET
generic_params: "<[" generic_param ("," generic_param)* "]>"
generic_param : IDENTIFIER (class_extends)?

// Function declaration
func_decl: func_modifiers? FUNGSI IDENTIFIER generic_params? "(" params? ")" ":" type_annot statement* BERAKHIR ";"?
func_modifiers: func_modifier+
func_modifier: ASYNC | STATIC
params: param ("," param)*
param: IDENTIFIER ":" type_annot param_default?
param_default: "=" expression

// Class declaration - DIPERBAIKI
class_decl: CLASS IDENTIFIER class_extends? class_member* BERAKHIR ";"?
class_extends: EXTENDS IDENTIFIER

?class_member: constructor_decl | method_decl

// Constructor - bisa set properties dengan simpan.prop
constructor_decl: KONSTRUKTOR generic_params? "(" params? ")" ":" type_annot statement* BERAKHIR ";"?

// Method tanpa keyword fungsi
method_decl: method_modifiers? IDENTIFIER generic_params? "(" params? ")" ":" type_annot statement* BERAKHIR ";"?
method_modifiers: STATIC | ASYNC

// Type annotations
type_annot: union_type
union_type: primary_type ("|" primary_type)*
primary_type: basic_type | generic_type | func_type | array_type | paren_type | custom_type
basic_type: TEKS | ANGKA | KONDISI | KOSONG | TIADA | TIDAK_TAHU | APAPUN | ELEMEN | REGEX | OBJEK
generic_type: KAMUS "[" type_annot "," type_annot "]" | DAFTAR "[" type_annot "]" | custom_type (("<[" type_list "]>") | ("[" type_list "]"))
custom_type: IDENTIFIER
type_list: type_annot ("," type_annot)*
func_type: "(" func_type_params? ")" "=>" type_annot
func_type_params: type_annot ("," type_annot)*
array_type: primary_type "[" "]"
paren_type: "(" type_annot ")"

// Import/Export (unchanged)
import_stmt: import_from | import_namespace
import_from: DARI STRING IMPORT import_spec ";"?
import_namespace: IMPORT STRING ";"?
import_spec: import_default | import_named | import_all | import_mixed
import_default: IDENTIFIER
import_named: "{" import_list "}"
import_all: "*" AS IDENTIFIER
import_mixed: IDENTIFIER "," "{" import_list "}"
import_list: import_item ("," import_item)*
import_item: IDENTIFIER import_alias?
import_alias: AS IDENTIFIER
export_stmt: export_decl | export_named | export_all
export_decl: EXPORT DEFAULT? exportable
export_named: EXPORT "{" export_list "}" export_from? ";"?
export_all: EXPORT "*" AS IDENTIFIER DARI STRING ";"?
exportable: var_decl | func_decl | class_decl | IDENTIFIER
export_from: DARI STRING
export_list: export_item ("," export_item)*
export_item: IDENTIFIER export_alias?
export_alias: AS IDENTIFIER

// Control flow
if_stmt: JIKA expression ";"? MAKA statement* if_continuation
if_continuation: AKHIR SELAIN MAKA statement* BERAKHIR ";"?
               | AKHIR SELAIN JIKA expression ";"? MAKA statement* if_continuation
               | BERAKHIR ";"?

try_stmt: COBA MENCOBA statement* try_continuation
try_continuation: AKHIR TANGKAP "("? IDENTIFIER ")"? LAKUKAN statement* try_finally_or_end | try_finally_or_end
try_finally_or_end: AKHIR AKHIRNYA ";"? LAKUKAN statement* BERAKHIR ";"? | BERAKHIR ";"?

switch_stmt: PILAH expression ";"? MAKA switch_case* BERAKHIR ";"?
switch_case: case_clause | default_clause
case_clause: KASUS expression ";"? MAKA statement* AKHIR ";"?
default_clause: BAWAAN ";"? MAKA statement* AKHIR ";"?

while_stmt: SELAMA expression ";"? LAKUKAN statement* BERAKHIR ";"?
do_stmt: KETIKA expression ";"? LAKUKAN statement* BERAKHIR ";"?
for_stmt: for_c_style | for_in_style
for_c_style: UNTUK "("? for_init? ";" expression? ";" expression? ";"? ")"? LAKUKAN statement* BERAKHIR ";"?
for_in_style: UNTUK "("? for_var DALAM expression ")"? ";"? LAKUKAN statement* BERAKHIR ";"?
for_init: var_decl | expression
for_var: var_modifier? IDENTIFIER ":" type_annot

return_stmt: KEMBALIKAN expression? ";"?
break_stmt: BERHENTI ";"?
continue_stmt: LANJUT ";"?
throw_stmt: LEMPAR expression ";"?

// Expressions - DIPERBAIKI untuk mendukung simpan/simpanan dan panggil
expr_stmt: expression ";"?
expression: assignment
assignment: conditional assign_op assignment | conditional
assign_op: "=" | "+=" | "-=" | "*=" | "/=" | "%=" | "**="
conditional: logical_or ("?" expression ":" conditional)?
logical_or: logical_and (("||" | ATAU) logical_and)*
logical_and: bitwise_or (("&&" | DAN) bitwise_or)*
bitwise_or: bitwise_xor ("|" bitwise_xor)*
bitwise_xor: bitwise_and ("^" bitwise_and)*
bitwise_and: equality ("&" equality)*
equality: relational (("==" | "!=") relational)*
relational: add (("<" | ">" | "<=" | ">=" | DALAM) add)*
add: minus ("+" minus)*
minus: multi ("-" multi)*
multi: divided ("*" divided)*
divided: moduler ("/" moduler)*
moduler: exponential ("%" exponential)*
exponential: unary ("**" exponential)*
unary: unary_prefix | await_expr | postfix
unary_prefix: ("+" | "-" | "~" | "!" | TIDAK | TIPE_DARI | HAPUS) unary | ("++" | "--") unary
await_expr: MENUNGGU expression
postfix: primary postfix_op*
postfix_op: member_access | computed_access | call_expr | postfix_incr
member_access: acc_succes | acc_option
acc_succes: "." IDENTIFIER
acc_option: ".?" IDENTIFIER
computed_access: "[" expression "]"
call_expr: "(" arg_list? ")"
postfix_incr: "++" | "--"

primary: literal | identifier | array_expr | object_expr | arrow_func | paren_expr | this_expr | super_expr | spread_expr | instantiation

literal: STRING | NUMBER | BOOLEAN | null_literal | element_expr
identifier: IDENTIFIER
paren_expr: "(" expression ")"

// DIPERBAIKI: this menggunakan simpan/simpanan
this_expr: INI | SIMPANAN

super_expr: INDUK
spread_expr: "..." primary
null_literal: KOSONG | TIADA

// DITAMBAH: instantiation dengan panggil
instantiation: initation | part_initation
initation: "(" part_initation ")"
part_initation: PANGGIL IDENTIFIER "(" arg_list? ")"

array_expr: "[" array_elements? "]"
array_elements: array_element ("," array_element)* ","?
array_element: expression

object_expr: "{" object_props? "}"
object_props: object_prop ("," object_prop)* ","?
object_prop: prop_key ":" expression | shorthand_prop | spread_prop
prop_key: IDENTIFIER | STRING | computed_prop
computed_prop: "[" expression "]"
shorthand_prop: IDENTIFIER
spread_prop: "..." expression

arrow_func: "(" params? ")" arrow_return? MAKA statement* BERAKHIR
arrow_return: ":" type_annot

element_expr: element_open element_content* element_close | element_self_close
element_open: "<" IDENTIFIER element_attrs? ">"
element_close: "</" IDENTIFIER ">"
element_self_close: "<" IDENTIFIER element_attrs? "/>"
element_attrs: element_attr+
element_attr: IDENTIFIER ("=" element_attr_val)?
element_attr_val: STRING | "{" expression "}"
element_content: element_expr | STRING | "{" expression "}"

arg_list: expression ("," expression)*

// Acoding
acoding_stmt: "#" ACODING ":" acoding_type
acoding_type: XML | MODULAR | SCRIPT | CONFIG

// Terminals
VAR: "variabel"
LET: "buatkan"
CONST: "tetapkan"
ANTARMUKA: "antarmuka"
TIPE: "tipe"
ENUM: "enum"
FUNGSI: "fungsi"
CLASS: "kelas"
KONSTRUKTOR: "konstruktor"
STATIC: "statis"
HANYA_DIBACA: "hanyaDibaca"
EXTENDS: "diperluasKe"
ASYNC: "singkronkan"
MENUNGGU: "menunggu"
IMPORT: "impor"
EXPORT: "ekspor"
DARI: "dari"
AS: "sebagai"
DEFAULT: "bawaan"
JIKA: "jika"
SELAIN: "selain"
UNTUK: "untuk"
SELAMA: "selama"
LAKUKAN: "lakukan"
KETIKA: "ketika"
PILAH: "pilahkan"
KASUS: "kasus"
BAWAAN: "bawaan"
BERHENTI: "berhentikan"
LANJUT: "lanjutkan"
KEMBALIKAN: "kembalikan"
COBA: "coba"
MENCOBA: "mencoba"
TANGKAP: "tangkap"
AKHIRNYA: "akhirnya"
LEMPAR: "lemparkan"
DALAM: "dalam"
MAKA: "maka"
AKHIR: "akhir"
BERAKHIR: "berakhir"
TEKS: "teks"
ANGKA: "angka"
KONDISI: "kondisi"
KOSONG: "kosong"
TIADA: "tiada"
TIDAK_TAHU: "tidakTahu"
APAPUN: "apapun"
ELEMEN: "elemen"
OBJEK: "objek"
KAMUS: "kamus"
DAFTAR: "daftar"
REGEX: "regex"
ATAU: "atau"
DAN: "dan"
TIDAK: "tidak"
TIPE_DARI: "tipeDari"
HAPUS: "hapuskan"
INI: "simpan"
SIMPANAN: "simpanan"
INDUK: "masukanInduk"
PANGGIL: "panggil"  // DITAMBAH
ACODING: "acoding"
XML: "xml"
MODULAR: "modular"
SCRIPT: "script"
CONFIG: "config"

BOOLEAN: "benar" | "salah"
NUMBER: /\d+(\.\d+)?/
STRING: /"[^"]*"/ | /'[^']*'/
IDENTIFIER: /[a-zA-Z_$][a-zA-Z0-9_$]*/
ID_GENERIC: /[a-zA-Z_$][a-zA-Z0-9_$]*<\[/

%import common.WS
%ignore WS
%ignore /\/\/[^\r\n]*/
%ignore /\/\*(.|\n)*?\*\//
"""
