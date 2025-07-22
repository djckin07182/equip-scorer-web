
import streamlit as st
from st_img_pastebutton import paste
from paddleocr import PaddleOCR
from PIL import Image
import base64
from io import BytesIO
import numpy as np

st.set_page_config(page_title="OCR 詞條辨識", layout="centered")
st.title("📷 OCR 圖片辨識")

image_data = paste(label="📋 點此貼上剪貼簿中的裝備截圖")

if image_data:
    header, encoded = image_data.split(",", 1)
    binary_data = base64.b64decode(encoded)
    image = Image.open(BytesIO(binary_data))

    st.image(image, caption="你貼上的圖片", use_container_width=True)

    with st.spinner("🔍 正在辨識文字..."):
        ocr = PaddleOCR(use_textline_orientation=True, lang='ch')
        img_array = np.array(image.convert("RGB"))
        result = ocr.ocr(img_array)

    st.subheader("📄 辨識結果：")
    for line in result[0]:
        if isinstance(line[1], list) and len(line[1]) >= 2:
            text = line[1][0]
            score = line[1][1]
        else:
            text = str(line[1])
            score = 0.0
        st.markdown(f"- **{text}**（信心分數：{score:.2f}）")
else:
    st.info("請先使用鍵盤截圖（Win+Shift+S）將畫面複製，再點擊上方按鈕貼上圖片。")
