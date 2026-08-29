"""Vākya token definitions and token types."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    # Keywords
    CHARA = auto()          # chara (var)
    DHRUVA = auto()         # dhruva (const)
    KARYA = auto()          # karya (fn)
    PRATYAVARTAYA = auto()  # pratyavartaya (return)
    YADI = auto()           # yadi (if)
    ANYATHA = auto()        # anyatha (else)
    TARHI = auto()          # tarhi (then)
    YAVAT = auto()          # yavat (while)
    PRATYEKAM = auto()      # pratyekam (for-each)
    MADHYE = auto()         # madhye (in)
    VIRAMA = auto()         # virama (break)
    AGACCHA = auto()        # agaccha (continue)
    SATYA = auto()          # satya (true)
    ASATYA = auto()         # asatya (false)
    SHUNYA = auto()         # shunya (null)
    AAYAT = auto()          # aayat (import)
    ANTAH = auto()          # antah (private)
    SARVAJAN = auto()       # sarvajan (public)
    EVAM = auto()           # evam (and)
    VA = auto()             # va (or)
    NA = auto()             # na (not)

    # Identifiers & Literals
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    # Operators
    PLUS = auto()           # +
    MINUS = auto()          # -
    STAR = auto()           # *
    SLASH = auto()          # /
    PERCENT = auto()        # %
    POWER = auto()          # **

    # Comparison
    EQ_EQ = auto()          # ==
    NOT_EQ = auto()         # !=
    LT = auto()             # <
    GT = auto()             # >
    LT_EQ = auto()          # <=
    GT_EQ = auto()          # >=

    # Assignment
    EQ = auto()             # =
    PLUS_EQ = auto()        # +=
    MINUS_EQ = auto()       # -=
    STAR_EQ = auto()        # *=
    SLASH_EQ = auto()       # /=

    # Punctuation & Delimiters
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    COMMA = auto()          # ,
    COLON = auto()          # :
    DOT = auto()            # .
    ARROW = auto()          # ->

    # Special
    EOF = auto()


KEYWORDS: dict[str, TokenType] = {
    "chara": TokenType.CHARA,
    "dhruva": TokenType.DHRUVA,
    "karya": TokenType.KARYA,
    "pratyavartaya": TokenType.PRATYAVARTAYA,
    "yadi": TokenType.YADI,
    "anyatha": TokenType.ANYATHA,
    "tarhi": TokenType.TARHI,
    "yavat": TokenType.YAVAT,
    "pratyekam": TokenType.PRATYEKAM,
    "madhye": TokenType.MADHYE,
    "virama": TokenType.VIRAMA,
    "agaccha": TokenType.AGACCHA,
    "satya": TokenType.SATYA,
    "asatya": TokenType.ASATYA,
    "shunya": TokenType.SHUNYA,
    "aayat": TokenType.AAYAT,
    "antah": TokenType.ANTAH,
    "sarvajan": TokenType.SARVAJAN,
    "evam": TokenType.EVAM,
    "va": TokenType.VA,
    "na": TokenType.NA,
}


@dataclass
class Token:
    """Represents a token produced by the lexical analyzer."""

    type: TokenType
    value: Any
    line: int
    column: int
    start_pos: int
    end_pos: int
    filename: str = "<anonymous>"

    @property
    def length(self) -> int:
        return max(1, self.end_pos - self.start_pos)

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"
