# tests/test_setup_auth.py
import pytest
from pages.login_page import LoginPage
from config.settings import AUTH_STATE_FILE
@pytest.mark.auth_setup
def test_save_login_state(page):
    login_page = LoginPage(page)
    
    # 1. Mở trang và đăng nhập
    login_page.open_url("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    
    # 2. Đợi danh sách sản phẩm xuất hiện để chắc chắn đã vào trong thành công
    page.locator(".inventory_list").wait_for(state="visible", timeout=10000)
    assert "inventory.html" in page.url

    # 3. Tạo thư mục và xuất state
    AUTH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    page.context.storage_state(path=str(AUTH_STATE_FILE))
    
    print(f"\n[AUTH SUCCESS] Đã lưu cookie và session vào: {AUTH_STATE_FILE}")