
from trait_service import load_trait_info
from models import Equipment

class EquipmentScorer:
    def __init__(self, trait_info=None):
        self.trait_info = trait_info or load_trait_info()
        self.messages = []

    def score(self, equipment: Equipment, weights: dict = None) -> float:
        self.messages.clear()
        total_score = 0
        part = equipment.part

        for field, trait in equipment.traits.items():
            if trait.value is None:
                continue

            key = f"{part}|{trait.field}|{trait.name}"
            info = self.trait_info.get(key)
            if not info:
                self.messages.append(f"{field}「{trait.name}」無對應評分資料")
                continue

            min_val, max_val = info.get("min"), info.get("max")
            weight = weights.get(field, 1.0) if weights else 1.0

            if min_val is None or max_val is None:
                continue

            if not (min_val <= trait.value <= max_val):
                self.messages.append(f"{field}「{trait.name}」超出範圍，未計入分數")
                continue

            ratio = (trait.value - min_val) / (max_val - min_val)
            score = ratio * 10 * weight
            total_score += score
            self.messages.append(f"{field}「{trait.name}」得分：{score:.2f}（權重：{weight}）")

        return total_score

    def calculate_pr(self, equipment: Equipment) -> float:
        total_ratio = 0
        count = 0
        part = equipment.part

        for field, trait in equipment.traits.items():
            if trait.value is None:
                continue
            key = f"{part}|{trait.field}|{trait.name}"
            info = self.trait_info.get(key)
            min_val, max_val = info.get("min"), info.get("max")
            if min_val is not None and max_val is not None and max_val > min_val:
                if min_val <= trait.value <= max_val:
                    ratio = (trait.value - min_val) / (max_val - min_val)
                    total_ratio += ratio
                    count += 1

        return round((total_ratio / count) * (count / 3) * 100, 2) if count > 0 else 0.0
