import os
import pytest
import allure
from pathlib import Path
from playwright.sync_api import Playwright, Page

# =========================================================================
# CẤU HÌNH ĐƯỜNG DẪN CƠ BẢN (Lùi 3 cấp về thư mục gốc)
# =========================================================================
BASE_DIR = Path(__file__).parent.parent.parent 
AUTH_STATE_FILE = BASE_DIR / "auth_state.json"


# =========================================================================
# GLOBAL SETUP: TỰ ĐỘNG ĐĂNG NHẬP VÀ LƯU PHIÊN (CHẠY 1 LẦN DUY NHẤT)
# =========================================================================
@pytest.fixture(scope="session", autouse=True)
def global_setup(playwright: Playwright):
    """Tự động đăng nhập và sinh file auth_state.json trước khi chạy toàn bộ Test Suites của SauceDemo."""
    print("\n[GLOBAL SETUP - SAUCEDEMO] Đang khởi tạo phiên đăng nhập...")
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    try:
        # Vào trang và đăng nhập bằng tài khoản hợp lệ
        page.goto("https://www.saucedemo.com/")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        
        # Chờ trang chuyển hướng thành công
        page.wait_for_url("**/inventory.html")
        
        # Lưu lại toàn bộ Cookie và Local Storage ra file
        context.storage_state(path=str(AUTH_STATE_FILE))
        print(f"[GLOBAL SETUP] Đã tạo thành công vé thông hành: {AUTH_STATE_FILE.name}")
    except Exception as e:
        print(f"\n[GLOBAL SETUP] Lỗi khi tạo auth_state: {e}")
    finally:
        browser.close()


# =========================================================================
# FIXTURE PAGE: Dành cho test chưa đăng nhập (Test Login, Quên MK...)
# =========================================================================
@pytest.fixture
def page(playwright: Playwright, request) -> Page:
    is_ci = os.getenv("CI", "false").lower() == "true"
    browser = playwright.chromium.launch(headless=is_ci)
    
    video_dir = BASE_DIR / "reports" / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)

    context = browser.new_context(
        record_video_dir=str(video_dir),
        record_video_size={"width": 1280, "height": 720}
    )
    page_instance = context.new_page()

    yield page_instance
    
    # --- SAU KHI TEST CHẠY XONG (TEARDOWN) ---
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        # A. CHỤP ẢNH MÀN HÌNH AN TOÀN
        try:
            if not page_instance.is_closed():
                page_instance.wait_for_timeout(500) # Nghỉ nửa giây ổn định UI
                screenshot_bytes = page_instance.screenshot(timeout=5000)
                allure.attach(
                    screenshot_bytes,
                    name=f"FAILED_SCREENSHOT_{request.node.name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"\n[CẢNH BÁO] Không thể chụp ảnh (Fixture page): {e}")

    # B. LẤY ĐƯỜNG DẪN VIDEO VÀ ĐÓNG TRÌNH DUYỆT AN TOÀN
    video_path = None
    try:
        video_path = page_instance.video.path() if page_instance.video else None
    except Exception:
        pass

    try:
        if not page_instance.is_closed():
            page_instance.close()
        context.close()
        browser.close()
    except Exception as e:
        print(f"\n[CẢNH BÁO] Lỗi khi đóng trình duyệt (Fixture page): {e}")

    # C. ĐÍNH KÈM VIDEO LÊN ALLURE VÀ XÓA FILE TẠM
    if failed and video_path and os.path.exists(video_path):
        with open(video_path, "rb") as v_file:
            allure.attach(
                v_file.read(),
                name=f"FAILED_EXECUTION_VIDEO_{request.node.name}",
                attachment_type=allure.attachment_type.WEBM
            )
    if video_path and os.path.exists(video_path):
        try:
            os.remove(video_path)
        except OSError:
            pass


# =========================================================================
# FIXTURE AUTHENTICATED_PAGE: Tái sử dụng phiên đăng nhập (Nghiệp vụ)
# =========================================================================
@pytest.fixture
def authenticated_page(playwright: Playwright, request) -> Page:
    is_ci = os.getenv("CI", "false").lower() == "true"
    browser = playwright.chromium.launch(headless=is_ci)

    video_dir = BASE_DIR / "reports" / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)

    context = browser.new_context(
        storage_state=str(AUTH_STATE_FILE),
        record_video_dir=str(video_dir),
        record_video_size={"width": 1280, "height": 720}
    )
    page_instance = context.new_page()

    yield page_instance

    # --- SAU KHI TEST CHẠY XONG (TEARDOWN) ---
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        # A. CHỤP ẢNH MÀN HÌNH AN TOÀN
        try:
            if not page_instance.is_closed():
                page_instance.wait_for_timeout(500)
                screenshot_bytes = page_instance.screenshot(timeout=5000)
                allure.attach(
                    screenshot_bytes,
                    name=f"FAILED_SCREENSHOT_{request.node.name}",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"\n[CẢNH BÁO] Không thể chụp ảnh (Fixture authenticated_page): {e}")

    # B. LẤY ĐƯỜNG DẪN VIDEO VÀ ĐÓNG TRÌNH DUYỆT AN TOÀN
    video_path = None
    try:
        video_path = page_instance.video.path() if page_instance.video else None
    except Exception:
        pass

    try:
        if not page_instance.is_closed():
            page_instance.close()
        context.close()
        browser.close()
    except Exception as e:
        print(f"\n[CẢNH BÁO] Lỗi khi đóng trình duyệt (Fixture authenticated_page): {e}")

    # C. ĐÍNH KÈM VIDEO LÊN ALLURE VÀ XÓA FILE TẠM
    if failed and video_path and os.path.exists(video_path):
        with open(video_path, "rb") as v_file:
            allure.attach(
                v_file.read(),
                name=f"FAILED_EXECUTION_VIDEO_{request.node.name}",
                attachment_type=allure.attachment_type.WEBM
            )
    if video_path and os.path.exists(video_path):
        try:
            os.remove(video_path)
        except OSError:
            pass