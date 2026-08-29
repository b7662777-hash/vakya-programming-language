"""Central machine-readable keyword registry for the Vākya programming language."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from vakya.lexer.tokens import TokenType


@dataclass(frozen=True)
class KeywordInfo:
    """Authoritative descriptor for a Vākya keyword or reserved identifier."""

    keyword: str
    devanagari: str
    sanskrit_meaning: str
    english_meaning: str
    token_type: Optional[TokenType]
    category: str
    reserved: bool
    version_introduced: str
    grammar_role: str
    example: str


KEYWORD_REGISTRY: Dict[str, KeywordInfo] = {
    # Variable & Constant Declarations
    "chara": KeywordInfo(
        keyword="chara",
        devanagari="चर",
        sanskrit_meaning="Movable / Changeable",
        english_meaning="Variable declaration",
        token_type=TokenType.CHARA,
        category="Declaration",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Declares a mutable variable binding",
        example='chara aayuhu = 16',
    ),
    "dhruva": KeywordInfo(
        keyword="dhruva",
        devanagari="ध्रुव",
        sanskrit_meaning="Fixed / Immutable / North Star",
        english_meaning="Constant declaration",
        token_type=TokenType.DHRUVA,
        category="Declaration",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Declares an immutable constant binding",
        example='dhruva pi = 3.14159',
    ),

    # Functions & Control Flow
    "karya": KeywordInfo(
        keyword="karya",
        devanagari="कार्य",
        sanskrit_meaning="Work / Action / Duty",
        english_meaning="Function declaration",
        token_type=TokenType.KARYA,
        category="Declaration",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Declares a named callable function or closure",
        example='karya yog(a: sankhya, b: sankhya) -> sankhya { pratyavartaya a + b }',
    ),
    "pratyavartaya": KeywordInfo(
        keyword="pratyavartaya",
        devanagari="प्रत्यावर्तय",
        sanskrit_meaning="Return / Turn back / Yield",
        english_meaning="Return statement",
        token_type=TokenType.PRATYAVARTAYA,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Returns a value from a function and exits the current call frame",
        example='pratyavartaya a + b',
    ),
    "yadi": KeywordInfo(
        keyword="yadi",
        devanagari="यदि",
        sanskrit_meaning="If / In case",
        english_meaning="Conditional if",
        token_type=TokenType.YADI,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Initiates a conditional branching block",
        example='yadi vayaha >= 18 { vada("Adult") }',
    ),
    "anyatha": KeywordInfo(
        keyword="anyatha",
        devanagari="अन्यथा",
        sanskrit_meaning="Otherwise / Else",
        english_meaning="Conditional else",
        token_type=TokenType.ANYATHA,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Defines the alternate branch of a conditional statement",
        example='anyatha { vada("Minor") }',
    ),
    "tarhi": KeywordInfo(
        keyword="tarhi",
        devanagari="तर्हि",
        sanskrit_meaning="Then / Therefore",
        english_meaning="Conditional then",
        token_type=TokenType.TARHI,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Optional delimiter for conditional blocks (reserved)",
        example='yadi satya tarhi { vada(1) }',
    ),
    "yavat": KeywordInfo(
        keyword="yavat",
        devanagari="यावत्",
        sanskrit_meaning="As long as / While / Unto",
        english_meaning="While loop",
        token_type=TokenType.YAVAT,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Initiates a condition-controlled repetitive loop",
        example='yavat count < 5 { count += 1 }',
    ),
    "pratyekam": KeywordInfo(
        keyword="pratyekam",
        devanagari="प्रत्येकम्",
        sanskrit_meaning="Each / Every one",
        english_meaning="For-each iteration",
        token_type=TokenType.PRATYEKAM,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Iterates over collections (lists, maps, strings)",
        example='pratyekam item madhye items { vada(item) }',
    ),
    "madhye": KeywordInfo(
        keyword="madhye",
        devanagari="मध्ये",
        sanskrit_meaning="Within / Among / Inside",
        english_meaning="In / Membership delimiter",
        token_type=TokenType.MADHYE,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Binds the loop variable to the target collection in for-each loops",
        example='pratyekam k madhye naksha { vada(k) }',
    ),
    "virama": KeywordInfo(
        keyword="virama",
        devanagari="विराम",
        sanskrit_meaning="Stop / Cessation / Break",
        english_meaning="Break loop",
        token_type=TokenType.VIRAMA,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Immediately terminates the enclosing while or for-each loop",
        example='yadi i == 10 { virama }',
    ),
    "agaccha": KeywordInfo(
        keyword="agaccha",
        devanagari="आगच्छ",
        sanskrit_meaning="Proceed / Advance / Continue",
        english_meaning="Continue loop",
        token_type=TokenType.AGACCHA,
        category="Control Flow",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Skips the remainder of the current loop iteration",
        example='yadi i % 2 == 0 { agaccha }',
    ),

    # Boolean & Null Literals
    "satya": KeywordInfo(
        keyword="satya",
        devanagari="सत्य",
        sanskrit_meaning="True / Truth / Reality",
        english_meaning="Boolean true",
        token_type=TokenType.SATYA,
        category="Literal",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Boolean truth literal",
        example='chara is_active = satya',
    ),
    "asatya": KeywordInfo(
        keyword="asatya",
        devanagari="असत्य",
        sanskrit_meaning="False / Untruth",
        english_meaning="Boolean false",
        token_type=TokenType.ASATYA,
        category="Literal",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Boolean falsehood literal",
        example='chara is_done = asatya',
    ),
    "shunya": KeywordInfo(
        keyword="shunya",
        devanagari="शून्य",
        sanskrit_meaning="Void / Empty / Zero / Null",
        english_meaning="Null value",
        token_type=TokenType.SHUNYA,
        category="Literal",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Absence of a value (Null / None)",
        example='chara result = shunya',
    ),

    # Logical Operators
    "evam": KeywordInfo(
        keyword="evam",
        devanagari="एवम्",
        sanskrit_meaning="And / Thus / Also",
        english_meaning="Logical AND",
        token_type=TokenType.EVAM,
        category="Operator",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Short-circuit logical conjunction",
        example='yadi a > 0 evam b > 0 { ... }',
    ),
    "va": KeywordInfo(
        keyword="va",
        devanagari="वा",
        sanskrit_meaning="Or / Either",
        english_meaning="Logical OR",
        token_type=TokenType.VA,
        category="Operator",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Short-circuit logical disjunction",
        example='yadi a == 0 va b == 0 { ... }',
    ),
    "na": KeywordInfo(
        keyword="na",
        devanagari="न",
        sanskrit_meaning="Not / Negation",
        english_meaning="Logical NOT",
        token_type=TokenType.NA,
        category="Operator",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Unary logical inversion (precedence level 8)",
        example='yadi na is_ready { ... }',
    ),

    # Modules & Access (Reserved)
    "aayat": KeywordInfo(
        keyword="aayat",
        devanagari="आयात",
        sanskrit_meaning="Import / Brought in",
        english_meaning="Module import",
        token_type=TokenType.AAYAT,
        category="Module",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Imports an external module or namespace",
        example='aayat ganita',
    ),
    "antah": KeywordInfo(
        keyword="antah",
        devanagari="अन्तः",
        sanskrit_meaning="Internal / Private / Within",
        english_meaning="Private visibility modifier",
        token_type=TokenType.ANTAH,
        category="Module",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Restricts symbol visibility to the current module",
        example='antah karya helper() { ... }',
    ),
    "sarvajan": KeywordInfo(
        keyword="sarvajan",
        devanagari="सर्वजन",
        sanskrit_meaning="Public / For all people",
        english_meaning="Public visibility modifier",
        token_type=TokenType.SARVAJAN,
        category="Module",
        reserved=True,
        version_introduced="1.0.0",
        grammar_role="Exports symbol for public consumption",
        example='sarvajan karya api() { ... }',
    ),

    # Security & Unsafe (Reserved for V3)
    "anumati": KeywordInfo(
        keyword="anumati",
        devanagari="अनुमति",
        sanskrit_meaning="Permission / Authorization",
        english_meaning="Capability permission declaration",
        token_type=None,
        category="Security",
        reserved=True,
        version_introduced="2.0.0",
        grammar_role="Declares explicit permission grant for capability security",
        example='anumati filesystem.read',
    ),
    "asurakshit": KeywordInfo(
        keyword="asurakshit",
        devanagari="असुरक्षित",
        sanskrit_meaning="Unsafe / Insecure / Unguarded",
        english_meaning="Unsafe block marker",
        token_type=None,
        category="Security",
        reserved=True,
        version_introduced="2.0.0",
        grammar_role="Encloses explicitly unverified low-level memory operations",
        example='asurakshit { ... }',
    ),

    # Built-in Type Names
    "sankhya": KeywordInfo(
        keyword="sankhya",
        devanagari="संख्या",
        sanskrit_meaning="Number / Integer",
        english_meaning="Integer type",
        token_type=None,
        category="Type",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Type annotation for whole numbers (64-bit integer)",
        example='chara count: sankhya = 100',
    ),
    "dashamika": KeywordInfo(
        keyword="dashamika",
        devanagari="दशमिक",
        sanskrit_meaning="Decimal / Fractional",
        english_meaning="Floating-point type",
        token_type=None,
        category="Type",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Type annotation for IEEE-754 double precision floating point numbers",
        example='chara rate: dashamika = 3.14',
    ),
    "shabda": KeywordInfo(
        keyword="shabda",
        devanagari="शब्द",
        sanskrit_meaning="Word / Sound / Text",
        english_meaning="String type",
        token_type=None,
        category="Type",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Type annotation for UTF-8 encoded text strings",
        example='chara name: shabda = "Arjuna"',
    ),
    "boolean": KeywordInfo(
        keyword="boolean",
        devanagari="बूलियन",
        sanskrit_meaning="Truth value",
        english_meaning="Boolean type",
        token_type=None,
        category="Type",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Type annotation for boolean values (satya / asatya)",
        example='chara ok: boolean = satya',
    ),
    "suchi": KeywordInfo(
        keyword="suchi",
        devanagari="सूची",
        sanskrit_meaning="List / Index / Needle",
        english_meaning="List / Array type",
        token_type=None,
        category="Type",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Type annotation for dynamic array collections",
        example='chara nums: suchi = [1, 2, 3]',
    ),
    "naksha": KeywordInfo(
        keyword="naksha",
        devanagari="नक्शा",
        sanskrit_meaning="Map / Chart / Plan",
        english_meaning="Map / Dictionary type",
        token_type=None,
        category="Type",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Type annotation for key-value hash map collections",
        example='chara user: naksha = {"name": "Goku"}',
    ),

    # Standard Builtin Functions
    "vada": KeywordInfo(
        keyword="vada",
        devanagari="वद",
        sanskrit_meaning="Speak / Say / Utter",
        english_meaning="Print / Output function",
        token_type=None,
        category="Builtin",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Standard builtin function printing arguments to stdout",
        example='vada("Namaste, World!")',
    ),
    "puchha": KeywordInfo(
        keyword="puchha",
        devanagari="पृच्छ",
        sanskrit_meaning="Ask / Inquire",
        english_meaning="Input function",
        token_type=None,
        category="Builtin",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Standard builtin reading a line from stdin with optional prompt",
        example='chara name = puchha("Name: ")',
    ),
    "lamba": KeywordInfo(
        keyword="lamba",
        devanagari="लम्ब",
        sanskrit_meaning="Length / Extent",
        english_meaning="Length function",
        token_type=None,
        category="Builtin",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Returns the number of elements in a list, map, or string",
        example='chara count = lamba(items)',
    ),
    "prakaar": KeywordInfo(
        keyword="prakaar",
        devanagari="प्रकार",
        sanskrit_meaning="Type / Kind / Species",
        english_meaning="Type-of function",
        token_type=None,
        category="Builtin",
        reserved=False,
        version_introduced="1.0.0",
        grammar_role="Returns the runtime type string of any value",
        example='chara t = prakaar(42) // "sankhya"',
    ),
}


def is_keyword(word: str) -> bool:
    """Check whether a string identifier is a registered Vākya keyword."""
    return word in KEYWORD_REGISTRY and KEYWORD_REGISTRY[word].reserved


def get_keyword_info(word: str) -> Optional[KeywordInfo]:
    """Retrieve metadata for a keyword or built-in identifier."""
    return KEYWORD_REGISTRY.get(word)


def get_lexer_keywords() -> Dict[str, TokenType]:
    """Return dictionary of keywords that have dedicated TokenTypes for the lexer."""
    return {
        k: v.token_type
        for k, v in KEYWORD_REGISTRY.items()
        if v.token_type is not None
    }
