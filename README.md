# Chatbot Tài Liệu Riêng

Ứng dụng Streamlit + LangChain + OpenAI, cho phép tải tài liệu lên và hỏi đáp trực tiếp.

## Cách chạy:
1. Cài thư viện:
```
pip install -r requirements.txt
```
2. Chạy ứng dụng:
```
streamlit run chatbot.py
```

## Ghi chú
- Nhớ tạo file `.streamlit/secrets.toml` để lưu API Key OpenAI.
- Các file đã upload sẽ tự động được lưu FAISS để lần sau sử dụng nhanh hơn.
