"""Handwritten lexical analyzer for Vākya."""

from typing import List, Optional
from ..errors import (
    LexerError,
    E001_INVALID_CHAR,
    E002_UNTERMINATED_STRING,
    E003_UNTERMINATED_COMMENT,
    E004_INVALID_ESCAPE,
    E005_INVALID_NUMBER,
)
from .tokens import Token, TokenType, KEYWORDS


class Lexer:
    """Scans Vākya source code and emits tokens."""

    def __init__(self, source: str, filename: str = "<anonymous>"):
        if source.startswith("\ufeff"):
            source = source[1:]
        self.source = source
        self.filename = filename
        self.length = len(source)
        self.pos = 0
        self.line = 1
        self.column = 1

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx >= self.length:
            return "\0"
        return self.source[idx]

    def _advance(self) -> str:
        if self.pos >= self.length:
            return "\0"
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while self.pos < self.length:
            ch = self._peek()

            # Skip whitespace
            if ch in " \t\r\n":
                self._advance()
                continue

            # Comments
            if ch == "/":
                next_ch = self._peek(1)
                if next_ch == "/":
                    # Single-line comment
                    while self.pos < self.length and self._peek() != "\n":
                        self._advance()
                    continue
                elif next_ch == "*":
                    # Multi-line comment
                    start_line = self.line
                    start_col = self.column
                    start_pos = self.pos
                    self._advance()  # consume /
                    self._advance()  # consume *
                    terminated = False
                    while self.pos < self.length:
                        if self._peek() == "*" and self._peek(1) == "/":
                            self._advance()  # consume *
                            self._advance()  # consume /
                            terminated = True
                            break
                        self._advance()
                    if not terminated:
                        raise LexerError.from_info(
                            E003_UNTERMINATED_COMMENT,
                            "Comment was never closed",
                            filename=self.filename,
                            line=start_line,
                            column=start_col,
                            length=self.pos - start_pos,
                            source_code=self.source,
                        )
                    continue

            # Identifiers and keywords
            if (("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch == "_"):
                tokens.append(self._scan_identifier_or_keyword())
                continue

            # Numbers (integers and floats)
            if ch.isdigit():
                tokens.append(self._scan_number())
                continue

            # Strings
            if ch == '"':
                tokens.append(self._scan_string())
                continue

            # Multi-character & single-character operators
            start_line = self.line
            start_col = self.column
            start_pos = self.pos

            if ch == "+":
                self._advance()
                if self._match("="):
                    tokens.append(Token(TokenType.PLUS_EQ, "+=", start_line, start_col, start_pos, self.pos, self.filename))
                else:
                    tokens.append(Token(TokenType.PLUS, "+", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "-":
                self._advance()
                if self._match(">"):
                    tokens.append(Token(TokenType.ARROW, "->", start_line, start_col, start_pos, self.pos, self.filename))
                elif self._match("="):
                    tokens.append(Token(TokenType.MINUS_EQ, "-=", start_line, start_col, start_pos, self.pos, self.filename))
                else:
                    tokens.append(Token(TokenType.MINUS, "-", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "*":
                self._advance()
                if self._match("*"):
                    tokens.append(Token(TokenType.POWER, "**", start_line, start_col, start_pos, self.pos, self.filename))
                elif self._match("="):
                    tokens.append(Token(TokenType.STAR_EQ, "*=", start_line, start_col, start_pos, self.pos, self.filename))
                else:
                    tokens.append(Token(TokenType.STAR, "*", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "/":
                self._advance()
                if self._match("="):
                    tokens.append(Token(TokenType.SLASH_EQ, "/=", start_line, start_col, start_pos, self.pos, self.filename))
                else:
                    tokens.append(Token(TokenType.SLASH, "/", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "%":
                self._advance()
                tokens.append(Token(TokenType.PERCENT, "%", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "=":
                self._advance()
                if self._match("="):
                    tokens.append(Token(TokenType.EQ_EQ, "==", start_line, start_col, start_pos, self.pos, self.filename))
                else:
                    tokens.append(Token(TokenType.EQ, "=", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "!":
                self._advance()
                if self._match("="):
                    tokens.append(Token(TokenType.NOT_EQ, "!=", start_line, start_col, start_pos, self.pos, self.filename))
                else:
                    raise LexerError.from_info(
                        E001_INVALID_CHAR,
                        f"Unexpected character '!' (did you mean '!=' or logical 'na'?)",
                        filename=self.filename,
                        line=start_line,
                        column=start_col,
                        length=1,
                        source_code=self.source,
                        help_text="Use 'na' for logical NOT, or '!=' for not-equal comparison.",
                    )
            elif ch == "<":
                self._advance()
                if self._match("="):
                    tokens.append(Token(TokenType.LT_EQ, "<=", start_line, start_col, start_pos, self.pos, self.filename))
                else:
                    tokens.append(Token(TokenType.LT, "<", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == ">":
                self._advance()
                if self._match("="):
                    tokens.append(Token(TokenType.GT_EQ, ">=", start_line, start_col, start_pos, self.pos, self.filename))
                else:
                    tokens.append(Token(TokenType.GT, ">", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "(":
                self._advance()
                tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == ")":
                self._advance()
                tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "{":
                self._advance()
                tokens.append(Token(TokenType.LBRACE, "{", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "}":
                self._advance()
                tokens.append(Token(TokenType.RBRACE, "}", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "[":
                self._advance()
                tokens.append(Token(TokenType.LBRACKET, "[", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == "]":
                self._advance()
                tokens.append(Token(TokenType.RBRACKET, "]", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == ",":
                self._advance()
                tokens.append(Token(TokenType.COMMA, ",", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == ":":
                self._advance()
                tokens.append(Token(TokenType.COLON, ":", start_line, start_col, start_pos, self.pos, self.filename))
            elif ch == ".":
                self._advance()
                tokens.append(Token(TokenType.DOT, ".", start_line, start_col, start_pos, self.pos, self.filename))
            else:
                self._advance()
                raise LexerError.from_info(
                    E001_INVALID_CHAR,
                    f"Unexpected character {ch!r}",
                    filename=self.filename,
                    line=start_line,
                    column=start_col,
                    length=1,
                    source_code=self.source,
                )

        tokens.append(Token(TokenType.EOF, "", self.line, self.column, self.pos, self.pos, self.filename))
        return tokens

    def _scan_identifier_or_keyword(self) -> Token:
        start_line = self.line
        start_col = self.column
        start_pos = self.pos

        ident_chars = []
        while self.pos < self.length:
            ch = self._peek()
            if ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ch.isdigit() or ch == "_":
                ident_chars.append(self._advance())
            else:
                break

        name = "".join(ident_chars)
        tok_type = KEYWORDS.get(name, TokenType.IDENTIFIER)
        return Token(tok_type, name, start_line, start_col, start_pos, self.pos, self.filename)

    def _scan_number(self) -> Token:
        start_line = self.line
        start_col = self.column
        start_pos = self.pos

        num_chars = []
        while self.pos < self.length and self._peek().isdigit():
            num_chars.append(self._advance())

        is_float = False
        if self._peek() == "." and self._peek(1).isdigit():
            is_float = True
            num_chars.append(self._advance())  # consume .
            while self.pos < self.length and self._peek().isdigit():
                num_chars.append(self._advance())

        # Check for invalid trailing characters (e.g. 123abc)
        trailing_ch = self._peek()
        if ("a" <= trailing_ch <= "z") or ("A" <= trailing_ch <= "Z") or trailing_ch == "_":
            invalid_chars = []
            while self.pos < self.length and (("a" <= self._peek() <= "z") or ("A" <= self._peek() <= "Z") or self._peek().isdigit() or self._peek() == "_"):
                invalid_chars.append(self._advance())
            invalid_suffix = "".join(invalid_chars)
            invalid_token = "".join(num_chars) + invalid_suffix
            raise LexerError.from_info(
                E005_INVALID_NUMBER,
                f"Invalid number literal '{invalid_token}': identifiers cannot begin with digits",
                filename=self.filename,
                line=start_line,
                column=start_col,
                length=self.pos - start_pos,
                source_code=self.source,
                help_text="Separate the numeric literal and identifier with an operator or space.",
            )

        num_str = "".join(num_chars)
        if is_float:
            return Token(TokenType.FLOAT, float(num_str), start_line, start_col, start_pos, self.pos, self.filename)
        else:
            return Token(TokenType.INTEGER, int(num_str), start_line, start_col, start_pos, self.pos, self.filename)

    def _scan_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        start_pos = self.pos

        self._advance()  # consume opening "
        str_chars = []

        while self.pos < self.length:
            ch = self._peek()
            if ch == '"':
                self._advance()  # consume closing "
                val = "".join(str_chars)
                return Token(TokenType.STRING, val, start_line, start_col, start_pos, self.pos, self.filename)
            elif ch == "\\":
                self._advance()  # consume backslash
                esc_ch = self._peek()
                esc_col = self.column
                if esc_ch == "n":
                    str_chars.append("\n")
                    self._advance()
                elif esc_ch == "t":
                    str_chars.append("\t")
                    self._advance()
                elif esc_ch == "r":
                    str_chars.append("\r")
                    self._advance()
                elif esc_ch == "\\":
                    str_chars.append("\\")
                    self._advance()
                elif esc_ch == '"':
                    str_chars.append('"')
                    self._advance()
                else:
                    self._advance()
                    raise LexerError.from_info(
                        E004_INVALID_ESCAPE,
                        f"Unrecognized escape sequence '\\{esc_ch}'",
                        filename=self.filename,
                        line=self.line,
                        column=esc_col - 1,
                        length=2,
                        source_code=self.source,
                    )
            elif ch == "\n":
                raise LexerError.from_info(
                    E002_UNTERMINATED_STRING,
                    "String literal contains unescaped newline or is unterminated",
                    filename=self.filename,
                    line=start_line,
                    column=start_col,
                    length=self.pos - start_pos,
                    source_code=self.source,
                )
            else:
                str_chars.append(self._advance())

        raise LexerError.from_info(
            E002_UNTERMINATED_STRING,
            "Unterminated string literal at end of file",
            filename=self.filename,
            line=start_line,
            column=start_col,
            length=self.pos - start_pos,
            source_code=self.source,
        )
