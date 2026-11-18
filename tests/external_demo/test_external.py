import pytest
import allure

@allure.epic("Hệ thống Demo Mở rộng (External Site)")
@allure.feature("Tương tác các UI Elements cơ bản")
class TestExternalSite:

    @allure.story("Kiểm tra chức năng Thêm và Xóa Element")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("UI", "Dynamic")
    def test_add_remove_dynamic_elements(self, page):
        allure.dynamic.title("Tương tác độc lập: Thêm/Xóa phần tử động")
        allure.dynamic.description(
            "**Mục tiêu:** Chứng minh Framework có thể mở các Context hoàn toàn mới, "
            "không bị ảnh hưởng bởi file `auth_state.json` của SauceDemo khi chạy song song."
        )
        
        with allure.step("Bước 1: Truy cập trang The Internet Herokuapp"):
            page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
            
        with allure.step("Bước 2: Click nút 'Add Element' 3 lần"):
            add_button = page.locator("button[onclick='addElement()']")
            for _ in range(3):
                add_button.click()
                
        with allure.step("Bước 3: Xác minh có đúng 3 nút 'Delete' xuất hiện"):
            delete_buttons = page.locator(".added-manually")
            assert delete_buttons.count() == 3, f"Kỳ vọng 3 nút, thực tế: {delete_buttons.count()}"
            
        with allure.step("Bước 4: Xóa 1 phần tử và kiểm tra lại số lượng"):
            delete_buttons.first.click()
            assert delete_buttons.count() == 2, "Lỗi logic: Xóa 1 nút nhưng số lượng còn lại không đúng."

    @allure.story("Kiểm tra thao tác Checkbox")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.tag("UI", "Checkbox")
    def test_checkboxes(self, page):
        allure.dynamic.title("Tương tác độc lập: Bật/Tắt Checkbox")
        
        with allure.step("Bước 1: Truy cập trang Checkboxes"):
            page.goto("https://the-internet.herokuapp.com/checkboxes")
            
        with allure.step("Bước 2: Đảo ngược trạng thái của 2 checkbox"):
            checkbox_1 = page.locator("input[type='checkbox']").nth(0)
            checkbox_2 = page.locator("input[type='checkbox']").nth(1)
            
            # Checkbox 1 mặc định tắt -> bật nó lên
            checkbox_1.check()
            # Checkbox 2 mặc định bật -> tắt nó đi
            checkbox_2.uncheck()
            
        with allure.step("Bước 3: Xác minh trạng thái hiển thị"):
            assert checkbox_1.is_checked(), "[FAIL] Checkbox 1 chưa được bật."
            assert not checkbox_2.is_checked(), "[FAIL] Checkbox 2 chưa được tắt."

    @allure.story("Đăng nhập hệ thống ngoại lai (Form Auth)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("UI", "Auth")
    def test_independent_login(self, page):
        allure.dynamic.title("Tương tác độc lập: Đăng nhập bằng form")
        allure.dynamic.description(
            "**Kịch bản đặc biệt:** Test case này sẽ thực hiện đăng nhập vào Herokuapp "
            "trong khi các test case của SauceDemo đang chạy ngầm bằng file `auth_state.json`. "
            "Nếu pass, chứng tỏ Playwright đã cách ly hoàn toàn Cookie của 2 luồng."
        )
        
        with allure.step("Bước 1: Truy cập trang Login của Herokuapp"):
            page.goto("https://the-internet.herokuapp.com/login")
            
        with allure.step("Bước 2: Nhập tài khoản 'tomsmith' và mật khẩu"):
            page.fill("#username", "tomsmith")
            page.fill("#password", "SuperSecretPassword!")
            page.click("button[type='submit']")
            
        with allure.step("Bước 3: Xác minh banner thông báo đăng nhập thành công"):
            flash_message = page.locator("#flash").inner_text()
            assert "You logged into a secure area!" in flash_message, (
                f"\n[FAIL] Thông báo đăng nhập không khớp!\nThực tế nhận được: {flash_message}"
            )