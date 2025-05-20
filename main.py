import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI

st.set_page_config(page_title="دليل الطالب - سؤال وجواب", layout="centered")
st.title("📘 اسأل عن دليلك الجامعي")

pdf = st.file_uploader("📎 قم برفع دليل PDF", type="pdf")

question = st.text_input("✍️ اكتب سؤالك هنا")

if pdf and question:
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    prompt = (
        f"الملف التالي يحتوي على دليل الطالب. استخرج إجابة مناسبة على السؤال التالي فقط من هذا المحتوى.\n\n"
        f"السؤال: {question}\n\n"
        f"الدليل:\n{text[:3000]}"
    )

    client = OpenAI(api_key=st.secrets["openai_api_key"])
    with st.spinner("جاري البحث في الدليل..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        st.success("✅ تم العثور على الإجابة:")
        st.write(response.choices[0].message.content)
