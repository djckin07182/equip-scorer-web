
import streamlit as st
import json
import pandas as pd
from models import Equipment
from scorer import EquipmentScorer

st.set_page_config(page_title="📁 裝備管理", page_icon="📁", layout="wide")
st.title("📁 裝備管理")

scorer = EquipmentScorer()
st.session_state.setdefault("saved_equipments", {})

# --- 匯入 JSON ---
uploaded = st.file_uploader("⬆️ 匯入 JSON 裝備資料（如需重覆匯入，請重新整理頁面後再匯入)", type="json", key="uploaded_file_buffer")

if uploaded and not st.session_state.get("imported_once"):
    try:
        imported = json.load(uploaded)
        cleaned = {k.strip(): v for k, v in imported.items()}
        st.session_state["saved_equipments"] = cleaned
        st.session_state["imported_once"] = True
        st.success("✅ 匯入成功，資料已加入")
    except Exception as e:
        st.error(f"❌ 匯入失敗：{e}")

# --- 匯出 JSON ---
if st.download_button("⬇️ 匯出 JSON", json.dumps(st.session_state["saved_equipments"], ensure_ascii=False), file_name="裝備資料.json"):
    st.info("📦 JSON 檔案已準備好下載")

# --- 整理裝備資料 ---

records = []
if st.session_state["saved_equipments"]:
    for name, data in st.session_state["saved_equipments"].items():
        try:
            part = data["part"]
            trait_inputs = data["trait_inputs"]
            weights = data.get("weights", {})
            equipment = Equipment.from_raw_input(part, trait_inputs)
            score, _ = scorer.score(equipment, weights)
            pr = scorer.calculate_pr_without_weight(equipment)

            traits = []
            for field, trait_dict in trait_inputs.items():
                for t_name, t_value in trait_dict.items():
                    trait_key = f"{part}|{field}|{t_name}"
                    if t_value is not None and trait_key in scorer.trait_info:
                        min_val = scorer.trait_info[trait_key].get("min")
                        max_val = scorer.trait_info[trait_key].get("max")
                        if min_val is not None and max_val is not None and min_val <= t_value <= max_val:
                            traits.append(f"{field}: {t_name} +{t_value}")

            records.append({
                
                "✔": st.session_state.get("select_all_toggle", False),
                "名稱": name,
                "部位": part,
                "總分": round(score, 2),
                "PR": pr,
                "詞條": "｜".join(traits),
            })
        except Exception as e:
            st.warning(f"⚠️ 無法讀取「{name}」: {e}")

# --- 顯示表格與刪除勾選 ---
if records:
    select_all_col, delete_col, info_col = st.columns([1, 2, 6])
    with select_all_col:
        select_all = st.checkbox("✔ 全選", key="select_all_toggle")

    df = pd.DataFrame(records)

    edited = st.data_editor(
        data=df,
        column_config={
            "✔": st.column_config.CheckboxColumn("✔ 刪除", default=False),
            "名稱": st.column_config.Column("裝備ID", disabled=True)
        },
        use_container_width=True,
        num_rows="fixed"
    )

    
    selected_keys = edited[edited["✔"] == True]["名稱"].tolist()

    with delete_col:
        if selected_keys and st.button("❌ 刪除選取裝備", key="delete_selected_btn"):
            removed = []
            for key in selected_keys:
                if key in st.session_state["saved_equipments"]:
                    del st.session_state["saved_equipments"][key]
                    removed.append(key)
            st.success(f"✅ 已刪除 {len(removed)} 件裝備")
            st.rerun()

    with info_col:
        if selected_keys:
            st.caption(f"🧾 你已選 {len(selected_keys)} 件裝備")
        
else:
    st.info("尚未儲存任何裝備資料。")
