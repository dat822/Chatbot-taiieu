import streamlit as st
import os
import tempfile

from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Thiết lập API Key cho OpenAI
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

# Giao diện Streamlit
st.set_page_config(page_title="Lịch Sử Chatbot", page_icon="📜", layout="wide")
st.title("🎓 Chatbot Tài Liệu Riêng")
st.markdown("""
<style>
    .main {
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo biến vector_store
vector_store = None
retriever = None

# Nếu đã tồn tại FAISS local thì load lại
if os.path.exists("faiss_store/index.faiss"):
    st.info("📁 Đang sử dụng dữ liệu đã lưu từ trước.")
    embedder = OpenAIEmbeddings()
    vector_store = FAISS.load_local("faiss_store", embedder)
    retriever = vector_store.as_retriever()
else:
    # Upload tài liệu
    uploaded_files = st.file_uploader("📂 Chọn một hoặc nhiều tài liệu (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    all_documents = []

    if uploaded_files:
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(uploaded_file.read())
                temp_file_path = f.name

            # Đọc tài liệu
            if uploaded_file.name.endswith(".pdf"):
                loader = PyPDFLoader(temp_file_path)
            elif uploaded_file.name.endswith(".txt"):
                loader = TextLoader(temp_file_path)
            elif uploaded_file.name.endswith(".docx"):
                loader = Docx2txtLoader(temp_file_path)
            else:
                st.error("🚫 Định dạng file không được hỗ trợ.")
                continue

            documents = loader.load()
            all_documents.extend(documents)

        # Xử lý tài liệu
        splitter = RecursiveCharacterText
