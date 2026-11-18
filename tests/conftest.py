import pytest
import allure

# =========================================================================
# HOOK DÙNG CHUNG TOÀN CỤC: BẮT LỖI VÀ GỌI AI
# =========================================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    
    if report.when == "call" and report.failed:
        print("\n" + "="*50)
        print("🚨 PHÁT HIỆN TEST LỖI! ĐANG GỌI GEMINI AI...")
        try:
            error_log = report.longreprtext if hasattr(report, 'longreprtext') else str(report.longrepr)
            from utils.ai_analyzer import analyze_error
            ai_result = analyze_error(error_log)
            ai_text = str(ai_result) if ai_result else "⚠️ LỖI: Gemini trả về rỗng."
            allure.attach(ai_text, name="🤖 AI CHẨN ĐOÁN LỖI (Gemini)", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"Lỗi gọi AI: {e}", name="⚠️ LỖI GỌI AI", attachment_type=allure.attachment_type.TEXT)