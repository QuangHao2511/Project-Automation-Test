# tests/test_cart.py
import pytest 
import allure
from pages.cart_page import CartPage
@pytest.mark.smoke
@allure.title("Thêm sản phẩm vào giỏ hàng thành công")
@allure.epic("Quản lý Đơn hàng")
@allure.feature("Chức năng Giỏ hàng")
class TestCartScenarios:

    @allure.title("Thêm sản phẩm vào giỏ hàng thành công (Không cần Login lại)")
    def test_add_items_to_cart_success(self, authenticated_page):
        cart_page = CartPage(authenticated_page)

        with allure.step("1. Truy cập trực tiếp trang danh sách sản phẩm"):
            cart_page.open_url("https://www.saucedemo.com/inventory.html")
            
            # Kiểm tra xem có bị đá về login không
            assert "inventory.html" in authenticated_page.url, (
                f"Lỗi: Bị đá về trang login! URL hiện tại: {authenticated_page.url}"
            )

        with allure.step("2. Thêm balo và đèn xe đạp vào giỏ hàng"):
            cart_page.add_backpack_to_cart()
            cart_page.add_bike_light_to_cart()

        with allure.step("3. Xác minh số lượng hiển thị trên giỏ hàng là 2"):
            badge_count = cart_page.get_cart_badge_count()
            assert badge_count == "2", f"Kỳ vọng 2 sản phẩm nhưng thực tế là: {badge_count}"