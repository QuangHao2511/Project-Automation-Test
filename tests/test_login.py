# tests/test_login.py
import pytest
import allure
from pages.login_page import LoginPage
from config.settings import TEST_DATA_JSON
from utils.file_reader import load_json

# Tải toàn bộ danh sách kịch bản kiểm thử
test_cases = load_json(TEST_DATA_JSON)

@allure.epic("Hệ thống Xác thực (Authentication)")
@allure.feature("Chức năng Đăng nhập")
class TestLoginScenarios:

    @pytest.mark.parametrize(
        "case_id, test_input",
        test_cases.items(),
        ids=[f"[{k}] {v['title']}" for k, v in test_cases.items()]
    )
    def test_negative_login(self, page, case_id, test_input):
        # Thiết lập thông tin động cho Allure Report
        allure.dynamic.title(f"{case_id}: {test_input['title']}")
        allure.dynamic.description(
            f"Kiểm tra phản hồi của hệ thống đối với kịch bản: {test_input['title']}"
        )
        
        login_page = LoginPage(page)

        # Bước 1: Mở trang
        with allure.step("Bước 1: Điều hướng tới trang đăng nhập SauceDemo"):
            login_page.open_url("https://www.saucedemo.com/")

        # Bước 2: Thao tác đăng nhập
        with allure.step(f"Bước 2: Điền thông tin (User: '{test_input['username']}') và nhấn Đăng nhập"):
            login_page.login(test_input["username"], test_input["password"])

        # Bước 3: Xác thực kết quả
        with allure.step(f"Bước 3: Xác minh thông báo lỗi hiển thị chứa: '{test_input['expected_error']}'"):
            actual_error = login_page.get_error_message()
            assert test_input["expected_error"] in actual_error, (
                f"\n[FAIL] Thông báo lỗi không khớp!"
                f"\nKỳ vọng chứa: {test_input['expected_error']}"
                f"\nThực tế nhận được: {actual_error}"
            )