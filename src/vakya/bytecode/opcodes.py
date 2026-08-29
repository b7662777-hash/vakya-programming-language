"""Opcode definitions for the Vākya Bytecode Virtual Machine."""

from enum import IntEnum, auto


class OpCode(IntEnum):
    # Literals and Constants
    CONSTANT = 1
    NULL = 2
    TRUE = 3
    FALSE = 4

    # Stack Management
    POP = 5
    DUP = 6

    # Variable Access
    LOAD_LOCAL = 7
    STORE_LOCAL = 8
    LOAD_GLOBAL = 9
    STORE_GLOBAL = 10
    LOAD_UPVALUE = 11
    STORE_UPVALUE = 12

    # Arithmetic Operations
    ADD = 13
    SUBTRACT = 14
    MULTIPLY = 15
    DIVIDE = 16
    MODULO = 17
    POWER = 18

    # Unary Operations
    NEGATE = 19
    NOT = 20

    # Comparisons and Equality
    EQUAL = 21
    NOT_EQUAL = 22
    LESS = 23
    LESS_EQUAL = 24
    GREATER = 25
    GREATER_EQUAL = 26

    # Control Flow and Jumps
    JUMP = 27
    JUMP_IF_FALSE = 28
    JUMP_IF_TRUE = 29
    JUMP_IF_FALSE_OR_POP = 30
    JUMP_IF_TRUE_OR_POP = 31

    # Functions and Closures
    MAKE_CLOSURE = 32
    CALL = 33
    CALL_BUILTIN = 34
    RETURN = 35

    # Collections and Accessors
    BUILD_LIST = 36
    BUILD_MAP = 37
    INDEX = 38
    SET_INDEX = 39
    GET_MEMBER = 40

    # Execution Control
    HALT = 41

    # Modules
    IMPORT_MODULE = 42

    def __str__(self) -> str:
        return self.name
