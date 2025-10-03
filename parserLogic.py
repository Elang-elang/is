# parserLogic.py - Parser Logic untuk Expressions dan Operassi
from typing import Any
from lark import Transformer
from lexer import LexerIS

class ParserLogic(LexerIS):
    def __init__(self) -> None:
        self.logging: dict[str, Any] = {}
        super().__init__()

    # ================================================
    #             EXPRESSION STATEMENTS
    # ================================================

    def expr_stmt(self, items):
        # print(f"{items = }")
        return f"{items[0]};"

    def expression(self, items):
        # print(f"expr={items}")
        return items[0]

    # ================================================
    #             ASSIGNMENT OPERATIONS
    # ================================================
    
    def assignment(self, items):
        if len(items) == 3:
            left, op, right = items
            return f"{left} {op} {right}"
        return items[0]

    def assign_op(self, items):
        return items[0] if items else "="

    # ================================================
    #             CONDITIONAL EXPRESSIONS
    # ================================================
    
    def conditional(self, items):
        if len(items) == 1:
            return items[0]
        return f"{items[0]} ? {items[2]} : {items[4]}"

    # ================================================
    #             LOGICAL OPERATIONS
    # ================================================
    
    def logical_or(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        for i in range(1, len(items)):
            if str(items[i]) in ['||', 'atau']:
                result += " || "
            else:
                result += str(items[i])
        return result

    def logical_and(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        for i in range(1, len(items)):
            if str(items[i]) in ['&&', 'dan']:
                result += " && "
            else:
                result += str(items[i])
        return result

    # ================================================
    #             BITWISE OPERATIONS
    # ================================================
    
    def bitwise_or(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        for i in range(1, len(items)):
            if str(items[i]) == "|":
                result += " | "
            else:
                result += str(items[i])
        return result

    def bitwise_xor(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        for i in range(1, len(items)):
            if str(items[i]) == "^":
                result += " ^ "
            else:
                result += str(items[i])
        return result

    def bitwise_and(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        for i in range(1, len(items)):
            if str(items[i]) == "&":
                result += " & "
            else:
                result += str(items[i])
        return result

    # ================================================
    #             COMPARISON OPERATIONS
    # ================================================
    
    def equality(self, items):
        if len(items) == 1:
            return items[0]
        if len(items) == 3:
            return f"{items[0]} {items[1]} {items[2]}"
        return items[0]

    def relational(self, items):
        if len(items) == 1:
            return items[0]
        if len(items) == 3:
            op = str(items[1])
            if op == 'dalam':
                return f"{items[2]}.includes({items[0]})"
            return f"{items[0]} {items[1]} {items[2]}"
        return items[0]

    # ================================================
    #             ARITHMETIC OPERATIONS
    # ================================================
    
    def add(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        i = 0
        while i < len(items):
            operand = str(items[i + 1])
            result = f"{result} + {operand}"
            i += 2
        return result

    def minus(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        i = 0
        while i < len(items):
            operand = str(items[i + 1])
            result = f"{result} - {operand}"
            i += 2
        return result

    def multi(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        i = 1
        while i < len(items):
            operand = str(items[i + 1])
            result = f"{result} * {operand}"
            i += 2
        return result

    def divided(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        i = 0
        while i < len(items):
            operand = str(items[i + 1])
            result = f"{result} / {operand}"
            i += 2
        return result

    def moduler(self, items):
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        i = 0
        while i < len(items):
            operand = str(items[i + 1])
            result = f"{result} % {operand}"
            i += 2
        return result

    def exponential(self, items):
        if len(items) == 1:
            return items[0]
        if len(items) == 3:
            return f"{items[0]} ** {items[2]}"
        return items[0]

    # ================================================
    #             UNARY OPERATIONS
    # ================================================
    
    def unary(self, items):
        return items[0]

    def unary_prefix(self, items):
        if len(items) == 2:
            op, operand = items
            op_str = str(op)
            if op_str == 'tidak':
                return f"!{operand}"
            elif op_str == 'tipeDari':
                return f"typeof {operand}"
            elif op_str == 'hapuskan':
                return f"delete {operand}"
            return f"{op}{operand}"
        return items[0]

    # ================================================
    #             POSTFIX OPERATIONS
    # ================================================
    
    def postfix(self, items):
        # print(f"{items=}")
        if len(items) == 1:
            return items[0]
        
        result = str(items[0])
        for op in items[1:]:
            result += str(op)
        return result

    def postfix_op(self, items):
        return items[0]

    def postfix_incr(self, items):
        return items[0]

    # ================================================
    #             MEMBER ACCESS & FUNCTION CALLS
    # ================================================
    
    def member_access(self, items):
        # print(f"{items=}"
        return items[0]

    def acc_option(self, items):
        return f".?{items[0]}"

    def acc_succes(self, items):
        return f".{items[0]}"

    def computed_access(self, items):
        if len(items) > 1:
            return str(items)
        return f"[{items[0]}]"

    def call_expr(self, items):
        if items and len(items) > 0:
            return f"({items[0]})"
        return "()"

    def arg_list(self, items):
        return ", ".join([str(item) for item in items])

    # ================================================
    #             PRIMARY EXPRESSIONS
    # ================================================
    
    def primary(self, items):
        return items[0]

    def literal(self, items):
        return items[0]

    def identifier(self, items):
        return str(items[0])

    def paren_expr(self, items):
        return f"({items[0]})"

    def this_expr(self, items):
        return "this"

    def super_expr(self, items):
        return "super"

    def spread_expr(self, items):
        return f"...{items[0]}"

    # ================================================
    #             NULL LITERALS
    # ================================================
    
    def null_literal(self, items):
        null_value = str(items[0])
        if null_value == "kosong":
            return "void"
        elif null_value == "tiada":
            return "null"
        return "null"

    # ================================================
    #             AWAIT EXPRESSIONS
    # ================================================
    
    def await_expr(self, items):
        return f"await {items[1]}"

    # ================================================
    #             ARRAY EXPRESSIONS
    # ================================================
    
    def array_expr(self, items):
        if items and len(items) > 0:
            return f"[{items[0]}]"
        return "[]"

    def array_elements(self, items):
        return ", ".join([str(item) for item in items])

    def array_element(self, items):
        return items[0]

    # ================================================
    #             OBJECT EXPRESSIONS
    # ================================================
    
    def object_expr(self, items):
        if items and len(items) > 0:
            return f"{{ {items[0]} }}"
        return "{}"

    def object_props(self, items):
        return ", ".join([str(item) for item in items])

    def object_prop(self, items):
        return f"{items[0]}: {items[0]}"

    def prop_key(self, items):
        return items[0]

    def computed_prop(self, items):
        return f"[{items[0]}]"

    def shorthand_prop(self, items):
        return str(items[0])

    def spread_prop(self, items):
        return f"...{items[1]}"

    # ================================================
    #             INSTANTIATION
    # ================================================
    def instantiation(self, items):
        return items[0]

    def initation(self, items):
        return f"({items[0]})"

    def part_initation(self, items):
        # print(f"calls=", items)
        class_name = str(items[1])  # Skip '(' and 'panggil'

        if len(items) == 2:
            return f"new {class_name}()"

        argv = []
        for arg in items[2:]:
            argv.append(str(arg))

        args = ", ".join(argv) if argv else ""

        return f"new {class_name}({args})"
