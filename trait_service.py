
import json

TRAIT_INFO_PATH = "trait_info.json"

def load_trait_info():
    with open(TRAIT_INFO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
