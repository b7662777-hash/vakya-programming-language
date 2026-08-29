"""Vākya standard error codes and default messages."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ErrorInfo:
    code: str
    title: str
    default_help: Optional[str] = None


# Lexer Errors (E001 - E099)
E001_INVALID_CHAR = ErrorInfo("E001", "Invalid character", "Remove or replace the unrecognized character.")
E002_UNTERMINATED_STRING = ErrorInfo("E002", "Unterminated string literal", "Ensure the string is closed with a matching quotation mark (\").")
E003_UNTERMINATED_COMMENT = ErrorInfo("E003", "Unterminated multi-line comment", "Close the comment with '*/'.")
E004_INVALID_ESCAPE = ErrorInfo("E004", "Invalid escape sequence", "Use supported escape sequences: \\n, \\t, \\\\, \\\", \\r.")
E005_INVALID_NUMBER = ErrorInfo("E005", "Invalid number literal", "Verify the numeric format (e.g., 42 or 3.14).")

# Name & Declaration Errors (E101 - E199)
E101_UNDEFINED_VARIABLE = ErrorInfo("E101", "Undefined variable", "Declare the variable using 'chara' or 'dhruva' before using it.")
E102_UNDEFINED_FUNCTION = ErrorInfo("E102", "Undefined function", "Define the function using 'karya' before calling it.")
E103_CONSTANT_REASSIGNMENT = ErrorInfo("E103", "Cannot reassign constant", "Constants declared with 'dhruva' are immutable. Use 'chara' for mutable variables.")
E104_DUPLICATE_DECLARATION = ErrorInfo("E104", "Variable already declared in current scope", "Use a different name or remove the duplicate declaration.")
E105_INVALID_ASSIGNMENT_TARGET = ErrorInfo("E105", "Invalid assignment target", "Assignments must target a variable, index expression, or property.")

# Parser & Syntax Errors (E201 - E299)
E201_UNEXPECTED_TOKEN = ErrorInfo("E201", "Unexpected token", "Check the syntax around this token.")
E202_EXPECTED_TOKEN = ErrorInfo("E202", "Expected token", "Add the required punctuation or keyword.")
E203_EXPECTED_EXPRESSION = ErrorInfo("E203", "Expected expression", "Provide a valid expression (value, identifier, or operation).")
E204_INVALID_PARAM = ErrorInfo("E204", "Invalid parameter declaration", "Function parameters must be identifiers with optional ': type'.")
E205_INVALID_LOOP_SYNTAX = ErrorInfo("E205", "Invalid loop syntax", "Syntax: 'pratyekam <item> madhye <iterable> { ... }' or 'yavat <condition> { ... }'.")
E206_INVALID_BREAK_CONTINUE = ErrorInfo("E206", "Loop control statement outside loop", "'virama' and 'agaccha' can only be used inside a loop body.")
E207_INVALID_RETURN = ErrorInfo("E207", "Return statement outside function", "'pratyavartaya' can only be used inside a function body.")

# Runtime Errors (E301 - E399)
E301_DIVISION_BY_ZERO = ErrorInfo("E301", "Division by zero", "Ensure the divisor expression is non-zero before dividing.")
E302_INDEX_OUT_OF_BOUNDS = ErrorInfo("E302", "Index out of bounds", "Check that the index is within the valid range [0, length - 1].")
E303_KEY_NOT_FOUND = ErrorInfo("E303", "Key not found in map", "Ensure the key exists in the map or check with 'map[key]'.")
E304_RECURSION_LIMIT = ErrorInfo("E304", "Maximum recursion depth exceeded", "Ensure recursive functions have a well-defined base case.")
E305_NOT_CALLABLE = ErrorInfo("E305", "Value is not callable", "Only functions can be called with '()'.")
E306_RUNTIME_TYPE_ERROR = ErrorInfo("E306", "Invalid operation on runtime value", "Check the types of the operands at runtime.")
E307_INVALID_PROPERTY = ErrorInfo("E307", "Unknown property access", "Check the property name.")

# Type Checking Errors (E401 - E499)
E401_TYPE_MISMATCH = ErrorInfo("E401", "Type mismatch", "Ensure the assigned value matches the declared variable type.")
E402_ARGUMENT_TYPE_MISMATCH = ErrorInfo("E402", "Argument type mismatch", "Provide an argument matching the expected parameter type.")
E403_RETURN_TYPE_MISMATCH = ErrorInfo("E403", "Return type mismatch", "Ensure the returned value matches the function's annotated return type.")
E404_OPERATOR_TYPE_MISMATCH = ErrorInfo("E404", "Incompatible operand types", "The operator cannot be applied to operands of these types.")
E405_UNARY_TYPE_MISMATCH = ErrorInfo("E405", "Incompatible operand type for unary operator", "Check the operand type.")
E406_ARGUMENT_COUNT_MISMATCH = ErrorInfo("E406", "Incorrect number of arguments", "Pass the exact number of arguments required by the function signature.")
E407_NOT_INDEXABLE = ErrorInfo("E407", "Type is not indexable", "Indexing with '[]' is only supported on 'suchi', 'naksha', and 'shabda'.")
