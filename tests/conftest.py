# tests/conftest.py
import pytest
import allure
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from config.settings import AUTH_STATE_FILE

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "reports" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

@pytest.fixture(scope="session")
def browser_instance():
    """Khởi tạo Browser với giao diện hiển thị (Headed Mode)."""
    with sync_playwright() as p:
        # headless=False: BẬT giao diện trình duyệt
        # slow_mo=500: Làm chậm mỗi hành động 500ms để quan sát rõ thao tác
        browser = p.chromium.launch(headless=False, slow_mo=500)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def browser_context(browser_instance):
    context = browser_instance.new_context(viewport={"width": 1280, "height": 720})
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def authenticated_page(browser_instance):
    """Khởi tạo context đã nạp sẵn cookie/token session với giao diện bật lên."""
    if not AUTH_STATE_FILE.exists():
        pytest.fail(f"Chưa có file session: {AUTH_STATE_FILE}. Hãy chạy test_setup_auth.py trước!")
    
    # Nạp storage_state vào context mới
    context = browser_instance.new_context(
        storage_state=str(AUTH_STATE_FILE),
        viewport={"width": 1280, "height": 720}
    )
    page = context.new_page()
    yield page
    page.close()
    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page_instance = item.funcargs.get("page") or item.funcargs.get("authenticated_page")
        if page_instance:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            file_path = SCREENSHOT_DIR / file_name
            screenshot_bytes = page_instance.screenshot(path=str(file_path), full_page=True)
            
            allure.attach(
                screenshot_bytes,
                name=f"Failure Screenshot - {item.name}",
                attachment_type=allure.attachment_type.PNG
            )