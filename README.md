
# 🛡️ 裝備評分系統 Equip Scorer Web

這是一個專注於「裝備詞條評分」的 Web 應用，讓玩家可以快速輸入裝備的屬性詞條，並依據預設規則自動計算出裝備的整體品質評分（PR 值）。

---

## 📊 功能重點：裝備評分

### 🔎 評分依據
- 每條詞條會依據其設定的 **最小值 / 最大值** 計算出 PR（品質比率）
- PR 值範圍為 **0～100 分**
- 遺漏的詞條會視為 **PR = 0**
- 評分邏輯為每條 PR 值平均，再乘以固定基準（詞條數補正）

### 💡 總體評分演算法
1. 每條詞條計算 PR 比例 = `(value - min) / (max - min) * 100`
2. 若詞條數不足 3 條，補上 `0`
3. 最終 PR = 所有 PR 值平均（固定除以 3）

### 🏷️ 評級制度
- PR ≥ 90 ➜ `S 級`
- PR ≥ 75 ➜ `A 級`
- PR ≥ 60 ➜ `B 級`
- 其餘 ➜ `C 級`

---

## 🧰 關鍵檔案說明

| 檔案 | 說明 |
|------|------|
| `app.py` | 評分流程主程式，負責接收輸入並顯示 PR 結果 |
| `scorer.py` | 評分核心邏輯，定義計算公式與比率判斷 |
| `trait_info.json` | 詞條設定檔，包含各詞條的 min/max/weight |

---

## 🚀 如何啟動

```bash
git clone https://github.com/yourname/equip-scorer-web.git
cd equip-scorer-web
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛠️ 評分自訂化

你可以自由編輯 `trait_info.json`，調整每個詞條的：
- 最小值 / 最大值（影響得分比例）
- 權重值（未來可擴充用）

---

## 📜 授權

MIT License
