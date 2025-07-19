import streamlit as st
from models import Equipment
from scorer import EquipmentScorer
from trait_service import load_trait_info

st.set_page_config(page_title="🛡️ 裝備評分系統", page_icon="🛡️", layout="centered")
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
            default_weight = trait_info.get(f"{part}|{field}|{name}", {}).get("weight", 1.0)
            weight = st.number_input(f"{field} 權重", key=f"weight_{i}", value=default_weight, step=0.1, format="%.2f")
            trait_inputs[field] = {name: value}
            weights[field] = weight

if st.button("計算分數"):
    equipment = Equipment.from_raw_input(part, trait_inputs=trait_inputs)
    score, _ = scorer.score(equipment, weights=weights)
    _, real_pr = scorer.score(equipment, weights=weights)

    grade = "S" if real_pr >= 0.9 else "A" if real_pr >= 0.75 else "B" if real_pr >= 0.6 else "C"

    pure_grade = "S" if real_pr >= 90 else "A" if real_pr >= 75 else "B" if real_pr >= 60 else "C"
    pure_color = "green" if real_pr >= 90 else "orange" if real_pr >= 75 else "gray"
    st.markdown(f"📊 <span style='color:{pure_color}; font-size:20px'>PR：{real_pr:.2f}%　[{pure_grade}]</span>", unsafe_allow_html=True)

    if scorer.messages:
        st.write("🔍 詳細說明：")
        for msg in scorer.messages:
            st.markdown(f"- {msg}")

# --- 儲存目前裝備 ---
name = st.text_input("命名並儲存這件裝備", "")
if name and st.button("💾 儲存裝備"):
    st.session_state.setdefault("saved_equipments", {})
    st.session_state["saved_equipments"][name] = {
        "part": part,
        "trait_inputs": trait_inputs,
        "weights": weights,
    }
    st.success(f"已儲存裝備：{name}")
