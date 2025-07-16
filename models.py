
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Trait:
    field: str  # 詞條1 / 詞條2 / 詞條3
    name: str
    value: Optional[float]

@dataclass
class Equipment:
    part: str
    defense: float
    traits: Dict[str, Trait]  # key: 詞條1 / 詞條2 / 詞條3

    @staticmethod
    def from_raw_input(part: str, trait_inputs: Dict[str, Dict[str, Optional[float]]]) -> "Equipment":
        traits = {}
        for field, trait_dict in trait_inputs.items():
            for name, value in trait_dict.items():
                traits[field] = Trait(field=field, name=name, value=value)
        return Equipment(part=part, traits=traits)
