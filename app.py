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
        "詞條2": ["DEF", "FLEE", "MDEF", "HP自然恢復速度增加(%)", "SP自然恢復速度增加(%)", "受到治癒量增加", "變動詠唱時間減少",
                  "從無屬性敵人受到的物理傷害減少(%)", "從水屬性敵人受到的物理傷害減少(%)", "從地屬性敵人受到的物理傷害減少(%)",
                  "從火屬性敵人受到的物理傷害減少(%)", "從風屬性敵人受到的物理傷害減少(%)", "從毒屬性敵人受到的物理傷害減少(%)",
                  "從聖屬性敵人受到的物理傷害減少(%)", "從暗屬性敵人受到的物理傷害減少(%)", "從念屬性敵人受到的物理傷害減少(%)",
                  "從不死屬性敵人受到的物理傷害減少(%)", "從無屬性敵人受到的魔法傷害減少(%)", "從水屬性敵人受到的魔法傷害減少(%)",
                  "從地無屬性敵人受到的魔法傷害減少(%)", "從火無屬性敵人受到的魔法傷害減少(%)", "從風無屬性敵人受到的魔法傷害減少(%)",
                  "從毒無屬性敵人受到的魔法傷害減少(%)", "從聖無屬性敵人受到的魔法傷害減少(%)", "從暗無屬性敵人受到的魔法傷害減少(%)",
                  "從念無屬性敵人受到的魔法傷害減少(%)", "從不死屬性敵人受到的魔法傷害減少(%)"],
        "詞條3": ["MaxHP", "MaxSP", "對無型怪物的抗性增加(%)", "對不死型怪物的抗性增加(%)", "對動物型怪物的抗性增加(%)",
                  "對植物型怪物的抗性增加(%)", "對昆蟲型怪物的抗性增加(%)", "對魚貝型怪物的抗性增加(%)", "對惡魔型怪物的抗性增加(%)",
                  "對人類型怪物的抗性增加(%)", "對天使型怪物的抗性增加(%)", "對龍族怪物的抗性增加(%)"]
    },
    "披肩": {
        "詞條1": ["MaxHP", "MaxHP(%)", "MaxSP", "MaxSP(%)"],
        "詞條2": ["DEF", "FLEE", "MDEF", "受到治癒量增加", "變動詠唱時間減少"],
        "詞條3": ["MaxHP", "MaxSP", "對無型怪物的抗性增加(%)", "對不死型怪物的抗性增加(%)", "對動物型怪物的抗性增加(%)"]
    },
    "鞋子": {
        "詞條1": ["MaxHP", "MaxHP(%)", "MaxSP", "MaxSP(%)"],
        "詞條2": ["DEF", "FLEE", "MDEF", "HIT", "受到治癒量增加"],
        "詞條3": ["MaxHP", "MaxSP", "對無型怪物的抗性增加(%)", "對不死型怪物的抗性增加(%)", "對動物型怪物的抗性增加(%)"]
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