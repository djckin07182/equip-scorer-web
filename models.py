
from dataclasses import dataclass

@dataclass
class Trait:
    field: str
    name: str
    value: float

@dataclass
class Equipment:
    part: str
    traits: dict

    @staticmethod
    def from_raw_input(part: str, trait_inputs: dict):
        traits = {}
        for field, trait_data in trait_inputs.items():
            for name, value in trait_data.items():
                traits[field] = Trait(field=field, name=name, value=value)
        return Equipment(part=part, traits=traits)
