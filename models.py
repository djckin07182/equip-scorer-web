
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
    traits: Dict[str, Trait]  # key: 詞條1 / 詞條2 / 詞條3

    @staticmethod
    def from_raw_input(part: str, trait_inputs: Dict[str, Dict[str, Optional[float]]]) -> "Equipment":
        allowed_fields = ['詞條1', '詞條2', '詞條3']
        traits = []
        for field in allowed_fields:
            if field not in trait_inputs:
                continue
            data = trait_inputs[field]
            for name, value in data.items():
                traits.append(Trait(field=field, name=name, value=value))
        return Equipment(part=part, traits=traits)
