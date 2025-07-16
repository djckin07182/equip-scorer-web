
import streamlit as st
from models import Equipment
from scorer import EquipmentScorer
from trait_service import load_trait_info

st.set_page_config(page_title="裝備評分系統", layout="centered")
st.title("🛡️ 裝備評分系統")

trait_info = load_trait_info()
scorer = EquipmentScorer(trait_info)

trait_options_by_part = {
    "鎧甲": {
        "詞條1": ["MaxHP", "MaxHP(%)", "MaxSP", "MaxSP(%)"],
        "詞條2": ["DEF", "FLEE", "MDEF"],
        "詞條3": ["MaxHP", "MaxSP", "對無型怪物的抗性增加(%)"]
    }
}

# 動態預設權重
default_weights = {
    "鎧甲": {
        "詞條1": {"MaxHP": 0.05, "MaxHP(%)": 2.5, "MaxSP": 0.4, "MaxSP(%)": 2.5},
        "詞條2": {"DEF": 0.5, "FLEE": 1.0, "MDEF": 2.5},
        "詞條3": {"MaxHP": 0.05, "MaxSP": 0.4, "對無型怪物的抗性增加(%)": 2.5}
    }
}

part = st.selectbox("裝備部位", list(trait_options_by_part.keys()))
trait_inputs = {}
weights = {}

for i in range(1, 4):
    field = f"詞條{i}"
    options = trait_options_by_part.get(part, {}).get(field, [])
    if options:
        with st.expander(f"詞條{i}", expanded=(i == 1)):
            name = st.selectbox(f"{field} 名稱", options, key=f"name_{i}")
            value = st.number_input(f"{field} 數值", key=f"value_{i}", step=1, format="%d")
            default_weight = default_weights.get(part, {}).get(field, {}).get(name, 1.0)
            weight = st.number_input(f"{field} 權重", key=f"weight_{i}", value=default_weight, step=0.1, format="%.2f")
            trait_inputs[field] = {name: value}
            weights[field] = weight

if st.button("計算分數"):
    equipment = Equipment.from_raw_input(part, trait_inputs=trait_inputs)
    score = scorer.score(equipment, weights=weights)
    real_pr = scorer.calculate_pr(equipment)

    st.subheader(f"✨ 裝備總分：{score:.2f}")

    pure_grade = "S" if real_pr >= 90 else "A" if real_pr >= 75 else "B" if real_pr >= 60 else "C"
    pure_color = "green" if real_pr >= 90 else "orange" if real_pr >= 75 else "gray"
    st.markdown(f"📊 <span style='color:{pure_color}; font-size:20px'>PR：{real_pr:.2f}%　[{pure_grade}]</span>", unsafe_allow_html=True)

    if scorer.messages:
        st.write("🔍 詳細說明：")
        for msg in scorer.messages:
            st.markdown(f"- {msg}")
