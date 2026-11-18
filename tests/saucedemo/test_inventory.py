import pytest
import allure

@allure.epic("Hệ thống E-Commerce SauceDemo")
@allure.feature("Danh sách sản phẩm (Inventory)")
class TestInventoryScenarios:

    @allure.story("Sắp xếp sản phẩm theo giá và tên")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("sort_option, expected_first_item", [
        ("az", "Sauce Labs Backpack"),               # Tên A to Z
        ("za", "Test.allTheThings() T-Shirt (Red)"), # Tên Z to A
        ("lohi", "Sauce Labs Onesie"),               # Giá thấp đến cao
        ("hilo", "Sauce Labs Fleece Jacket")         # Giá cao xuống thấp
    ])
    def test_sort_products(self, authenticated_page, sort_option, expected_first_item):
        allure.dynamic.title(f"Kiểm tra chức năng sắp xếp với tùy chọn: {sort_option}")
        
        # Mở trang danh sách (do đã dùng authenticated_page nên sẽ vào thẳng)
        with allure.step("Vào trang danh sách sản phẩm"):
            authenticated_page.goto("https://www.saucedemo.com/inventory.html")
            
        # Tương tác với Dropdown
        with allure.step(f"Chọn chế độ sắp xếp: {sort_option}"):
            authenticated_page.locator(".product_sort_container").select_option(sort_option)
            
        # Lấy tên sản phẩm đầu tiên sau khi sắp xếp
        with allure.step("Xác minh sản phẩm đầu tiên hiển thị đúng chuẩn"):
            first_item_name = authenticated_page.locator(".inventory_item_name").first.inner_text()
            assert first_item_name == expected_first_item, (
                f"\n[FAIL] Lỗi sắp xếp {sort_option}!"
                f"\nKỳ vọng sản phẩm đầu tiên: {expected_first_item}"
                f"\nThực tế hiển thị: {first_item_name}"
            )