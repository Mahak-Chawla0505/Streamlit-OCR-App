import streamlit as st
from PIL import Image
import pytesseract
import io

# Optional: Set Tesseract path if not in system PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

st.set_page_config(page_title="🧠 OCR Text Extractor", layout="centered")

st.title("🧠 OCR Text Extractor")
st.markdown("Upload an image and extract text using Tesseract OCR.")

uploaded_file = st.file_uploader("📤 Upload Image", type=["png", "jpg", "jpeg", "bmp", "tiff"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("🔍 Extract Text"):
        with st.spinner("Running OCR..."):
            text = pytesseract.image_to_string(image)
        if text.strip():
            st.success("✅ Text extracted successfully!")
            st.text_area("📜 Extracted Text", text, height=300)

            # Download button
            text_bytes = io.BytesIO(text.encode("utf-8"))
            st.download_button("💾 Download Text", text_bytes, file_name="extracted_text.txt")
        else:
            st.warning("No text detected in the image.")

# Upload reference text
reference_file = st.file_uploader("📄 Upload Ground Truth Text (Optional)", type=["txt"])

# After OCR extraction
if st.button("🔍 Extract Text", key="extract_button"):
    with st.spinner("Running OCR..."):
        extracted_text = pytesseract.image_to_string(image)

    if extracted_text.strip():
        st.success("✅ Text extracted successfully!")
        st.text_area("📜 Extracted Text", extracted_text, height=300)

        # Accuracy comparison
        if reference_file:
            reference_text = reference_file.read().decode("utf-8")
            from difflib import SequenceMatcher
            similarity = SequenceMatcher(None, extracted_text.strip(), reference_text.strip()).ratio()
            st.metric("🧪 OCR Accuracy", f"{similarity * 100:.2f}%")