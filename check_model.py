import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Đọc file .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Đang kết nối để lấy danh sách Model...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Khả dụng: {m.name}")
except Exception as e:
    print("Lỗi:", e)