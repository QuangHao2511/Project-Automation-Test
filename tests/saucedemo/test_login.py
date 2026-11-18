import pytest
import allure
from pages.login_page import LoginPage

# =========================================================================
# TEST DATA TÁCH BIỆT (Tương lai có thể chuyển ra file JSON/Excel)
# =========================================================================
test_cases = {
    "TC01_LOCKED_USER": {
        "title": "Đăng nhập với tài khoản bị khóa",
        "username": "locked_out_user",
        "password": "secret_sauce",
        "expected_error": "Epic sadface: Sorry, this user has been locked out."
    },
    "TC02_NO_PASSWORD": {
        "title": "Đăng nhập không nhập mật khẩu",
        "username": "standard_user",
        "password": "",
        "expected_error": "Epic sadface: Password is required"
    },
    "TC03_WRONG_PASSWORD": {
        "title": "Nhập sai mật khẩu của tài khoản",
        "username": "standard_user",
        "password": "invalid_password_123",
        "expected_error": "Epic sadface: Username and password do not match any user in this service"
    }
}

# =========================================================================
# KỊCH BẢN KIỂM THỬ (TEST SCENARIOS)
# =========================================================================
@allure.epic("Hệ thống Xác thực Người dùng (Authentication)")
@allure.feature("Đăng nhập (Login)")
class TestLoginScenarios:

    @allure.story("Đăng nhập thất bại (Negative Flow)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("Regression", "UI", "Auth")
    @pytest.mark.parametrize(
        "case_id, test_input",
        test_cases.items(),
        ids=[f"[{k}] {v['title']}" for k, v in test_cases.items()]
    )
    def test_negative_login(self, page, case_id, test_input):
        # 1. THIẾT LẬP THÔNG TIN CHO BÁO CÁO ALLURE
        allure.dynamic.title(f"[{case_id}] {test_input['title']}")
        allure.dynamic.description(
            f"**Mục tiêu:** Kiểm tra phản hồi của hệ thống đối với kịch bản: {test_input['title']}\n\n"
            f"**Tài khoản test:** `{test_input['username']}` / `{test_input['password']}`\n\n"
            f"**Kết quả kỳ vọng:** Báo lỗi chính xác `{test_input['expected_error']}`"
        )

        login_page = LoginPage(page)

        # 2. THỰC THI CÁC BƯỚC TEST (STEPS)
        with allure.step("Bước 1: Điều hướng tới trang đăng nhập SauceDemo"):
            login_page.open_url("https://www.saucedemo.com/")

        with allure.step(f"Bước 2: Điền thông tin (User: '{test_input['username']}') và nhấn Đăng nhập"):
            login_page.login(test_input["username"], test_input["password"])

        # 3. KIỂM CHỨNG KẾT QUẢ (ASSERTION CHUẨN)
        with allure.step(f"Bước 3: Xác minh thông báo lỗi hiển thị chứa: '{test_input['expected_error']}'"):
            actual_error = login_page.get_error_message()
            
            # Khôi phục lại biến kỳ vọng, xóa câu đùa test AI
            assert test_input['expected_error'] in actual_error, (
                f"\n[FAIL] Thông báo lỗi không khớp!"
                f"\nKỳ vọng chứa: {test_input['expected_error']}"
                f"\nThực tế nhận được: {actual_error}"
            )