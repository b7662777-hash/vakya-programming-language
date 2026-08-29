"""Vākya type representation and type compatibility rules."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class VakyaType:
    name: str

    def is_assignable_to(self, target: "VakyaType") -> bool:
        if target.name == "unknown" or self.name == "unknown":
            return True
        if self.name == target.name:
            return True
        # Allow sankhya (int) to be passed where dashamika (float) is expected if needed
        if self.name == "sankhya" and target.name == "dashamika":
            return True
        return False

    def __str__(self) -> str:
        return self.name


# Primitive types
TYPE_SANKHYA = VakyaType("sankhya")      # int
TYPE_DASHAMIKA = VakyaType("dashamika")  # float
TYPE_SHABDA = VakyaType("shabda")        # string
TYPE_BOOLEAN = VakyaType("boolean")      # bool
TYPE_SUCHI = VakyaType("suchi")          # list
TYPE_NAKSHA = VakyaType("naksha")        # map
TYPE_SHUNYA = VakyaType("shunya")        # null
TYPE_UNKNOWN = VakyaType("unknown")      # dynamic / any


@dataclass(frozen=True)
class FunctionType(VakyaType):
    param_types: List[VakyaType]
    return_type: VakyaType

    def __init__(self, param_types: List[VakyaType], return_type: VakyaType):
        super().__init__(name="karya")
        object.__setattr__(self, "param_types", param_types)
        object.__setattr__(self, "return_type", return_type)

    def __str__(self) -> str:
        params_str = ", ".join(str(p) for p in self.param_types)
        return f"karya({params_str}) -> {self.return_type}"


NAME_TO_TYPE = {
    "sankhya": TYPE_SANKHYA,
    "dashamika": TYPE_DASHAMIKA,
    "shabda": TYPE_SHABDA,
    "boolean": TYPE_BOOLEAN,
    "suchi": TYPE_SUCHI,
    "naksha": TYPE_NAKSHA,
    "shunya": TYPE_SHUNYA,
    "unknown": TYPE_UNKNOWN,
}


def lookup_type(name: Optional[str]) -> VakyaType:
    if name is None:
        return TYPE_UNKNOWN
    return NAME_TO_TYPE.get(name.lower(), TYPE_UNKNOWN)
