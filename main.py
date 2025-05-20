import os
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

# تحميل مفاتيح البيئة
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="سؤال من PDF", layout="centered")
st.title("📄 استفسر من ملف PDF")

uploaded_file = st.file_uploader("📥 ارفع ملف PDF", type=["pdf"])

if uploaded_file:
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # استخراج النص من الملف
    loader = PyPDFLoader(temp_file_path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = FAISS.from_documents(texts, embeddings)
    chain = load_qa_chain(ChatOpenAI(openai_api_key=openai_api_key), chain_type="stuff")

    query = st.text_input("💬 ما سؤالك؟")

    if query:
        with st.spinner("جاري المعالجة..."):
            docs = db.similarity_search(query)
            answer = chain.run(input_documents=docs, question=query)
            st.success("✅ تم العثور على الإجابة:")
            st.write(answer)
else:
    st.info("يرجى رفع ملف PDF أولاً.")
