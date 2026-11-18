import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
import concurrent.futures

# Tải biến môi trường từ file .env
load_dotenv()

def analyze_error(error_log: str) -> str:
    """Gửi Error Log cho AI phân tích nguyên nhân rớt test."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Không tìm thấy GEMINI_API_KEY. Bỏ qua bước phân tích AI."

    # Cấu hình AI model
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.8-flash')
    
    prompt = f"""
    Bạn là một chuyên gia Automation Test. 
    Dưới đây là Error Log của test case FAILED:
    
    {error_log[:1500]} 
    
    Dựa vào log trên, hãy trả lời cực kỳ ngắn gọn:
    1. Nguyên nhân gốc rễ gây lỗi là gì?
    2. Gợi ý cách sửa lỗi chi tiết.
    """

    def _call_api():
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Ép API trả lời nhanh trong 20s, nếu lag văng lỗi luôn để qua vòng Retry mới
                response = model.generate_content(
                    prompt,
                    request_options={"timeout": 20}
                )
                return response.text
            except Exception as e:
                error_msg = str(e)
                if ("504" in error_msg or "503" in error_msg or "429" in error_msg) and attempt < max_retries - 1:
                    print(f"\n[AI RETRY] Server lag (Lần {attempt + 1}/{max_retries}). Đang đợi 3s để gọi lại...")
                    time.sleep(3)
                    continue
                raise e

  
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_call_api)
    
    try:
        # Nếu tổng thời gian (bao gồm cả retry) vượt quá 45 giây -> Cắt luồng luôn!
        return future.result(timeout=45)
    except concurrent.futures.TimeoutError:
        return "⚠️ BỎ QUA AI: Máy chủ API treo quá lâu, đã tự động chặt đứt kết nối để test chạy tiếp."
    except Exception as e:
        return f"⚠️ LỖI AI: Không thể phân tích ({str(e)})"
    finally:
        # CỰC KỲ QUAN TRỌNG: Tắt executor, hủy bỏ tương lai, KHÔNG ĐỢI luồng đang bị kẹt
        executor.shutdown(wait=False, cancel_futures=True)