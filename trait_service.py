
import json
from pathlib import Path

TRAIT_INFO_PATH = Path(__file__).parent / "trait_info.json"

def load_trait_info():
    with open(TRAIT_INFO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_trait_info(trait_info):
    with open(TRAIT_INFO_PATH, "w", encoding="utf-8") as f:
        json.dump(trait_info, f, ensure_ascii=False, indent=2)
