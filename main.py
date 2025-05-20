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
    max_pages = 3  # Only read the first 3 pages to reduce token usage
    for i, page in enumerate(reader.pages):
        if i >= max_pages:
            break
        page_text = page.extract_text()
        if page_text:
            text += page_text

    prompt = (
        f"الملف التالي يحتوي على دليل الطالب. استخرج إجابة مناسبة على السؤال التالي فقط من هذا المحتوى.\n\n"
        f"السؤال: {question}\n\n"
        f"الدليل:\n{text}"
    )

    client = OpenAI(api_key=st.secrets["openai_api_key"])
    with st.spinner("جاري البحث في الدليل..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            st.success("✅ تم العثور على الإجابة:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error("❌ حدث خطأ أثناء الاتصال بـ OpenAI. الرجاء المحاولة لاحقًا.")
            st.exception(e)
