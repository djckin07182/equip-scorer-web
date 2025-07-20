
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
uploaded = st.file_uploader("⬆️ 匯入 JSON 裝備資料", type="json")
if uploaded:
    try:
        imported = json.load(uploaded)
        st.session_state["saved_equipments"].update(imported)
        st.success("✅ 匯入成功，資料已加入")
    except Exception as e:
        st.error(f"❌ 匯入失敗：{e}")

# --- 匯出 JSON ---
if st.download_button("⬇️ 匯出 JSON", json.dumps(st.session_state["saved_equipments"], ensure_ascii=False), file_name="裝備資料.json"):
    st.info("📦 JSON 檔案已準備好下載")

# --- 匯出 CSV ---
if st.button("⬇️ 匯出成績 CSV"):
    records = []
    for name, data in st.session_state["saved_equipments"].items():
        equipment = Equipment.from_raw_input(data["part"], data["trait_inputs"])
        score, _ = scorer.score(equipment, weights=data["weights"])
        pr = scorer.calculate_pr_without_weight(equipment)

        traits = []
        for field, trait_dict in data["trait_inputs"].items():
            for t_name, t_value in trait_dict.items():
                trait_key = f"{data['part']}|{field}|{t_name}"
                if t_value is not None and trait_key in scorer.trait_info:
                    min_val = scorer.trait_info[trait_key].get("min")
                    max_val = scorer.trait_info[trait_key].get("max")
                    if min_val is not None and max_val is not None and min_val <= t_value <= max_val:
                        traits.append(f"{field}: {t_name} +{t_value}")

        records.append({
            "名稱": name,
            "部位": data["part"],
            "總分": round(score, 2),
            "PR": pr,
            "詞條": "｜".join(traits)
        })

    if records:
        df = pd.DataFrame(records)
        if "總分" in df.columns:
            df = df.sort_values("總分", ascending=False)
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("📥 下載 CSV", csv, file_name="裝備成績.csv")
    else:
        st.warning("目前沒有任何裝備資料可供匯出。")

# --- 顯示儲存裝備表格與刪除功能 ---
if st.checkbox("📊 顯示已儲存裝備清單", value=True):
    if st.session_state["saved_equipments"]:
        table = []
        for name, data in st.session_state["saved_equipments"].items():
            equipment = Equipment.from_raw_input(data["part"], data["trait_inputs"])
            score, _ = scorer.score(equipment, weights=data["weights"])
            pr = scorer.calculate_pr_without_weight(equipment)

            traits = []
            for field, trait_dict in data["trait_inputs"].items():
                for t_name, t_value in trait_dict.items():
                    trait_key = f"{data['part']}|{field}|{t_name}"
                    if t_value is not None and trait_key in scorer.trait_info:
                        min_val = scorer.trait_info[trait_key].get("min")
                        max_val = scorer.trait_info[trait_key].get("max")
                        if min_val is not None and max_val is not None and min_val <= t_value <= max_val:
                            traits.append(f"{field}: {t_name} +{t_value}")

            table.append({
                "名稱": name,
                "部位": data["part"],
                "總分": round(score, 2),
                "PR": pr,
                "詞條": "｜".join(traits)
            })

        df = pd.DataFrame(table).sort_values("總分", ascending=False)
        st.dataframe(df)

        to_delete = st.selectbox("選擇要刪除的裝備：", list(st.session_state["saved_equipments"].keys()))
        if st.button("🗑️ 確認刪除"):
            del st.session_state["saved_equipments"][to_delete]
            st.success(f"已刪除裝備：{to_delete}")
            import sys
            sys.exit()
    else:
        st.info("尚未儲存任何裝備資料。")
