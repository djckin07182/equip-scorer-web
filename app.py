import streamlit as st
from models import Equipment
from scorer import EquipmentScorer
from trait_service import load_trait_info

st.set_page_config(page_title="裝備評分系統", layout="centered")
st.title("🛡️ 裝備評分系統")

trait_info = load_trait_info()
scorer = EquipmentScorer(trait_info)
def build_trait_options(trait_info):
    options = {}
    for key in trait_info:
        part, field, name = key.split("|")
        options.setdefault(part, {}).setdefault(field, []).append(name)
    return options

trait_options_by_part = build_trait_options(trait_info)

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
            default_weight = scorer.trait_info.get(f"{part}|{field}|{name}", {}).get("weight", 1.0)
            weight = st.number_input(f"{field} 權重", key=f"weight_{i}", value=default_weight, step=0.1, format="%.2f")
            trait_inputs[field] = {name: value}
            weights[field] = weight

if st.button("計算分數"):
    equipment = Equipment.from_raw_input(part, trait_inputs=trait_inputs)
    score, _ = scorer.score(equipment, weights=weights)
    real_pr = scorer.calculate_pr(equipment)

    st.subheader(f"✨ 裝備總分：{score:.2f}")

    pure_grade = "S" if real_pr >= 90 else "A" if real_pr >= 75 else "B" if real_pr >= 60 else "C"
    pure_color = "green" if real_pr >= 90 else "orange" if real_pr >= 75 else "gray"
    st.markdown(f"📊 <span style='color:{pure_color}; font-size:20px'>PR：{real_pr:.2f}%　[{pure_grade}]</span>", unsafe_allow_html=True)

    if scorer.messages:
        st.write("🔍 詳細說明：")
        for msg in scorer.messages:
            st.markdown(f"- {msg}")