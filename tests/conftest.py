import os
import pytest
import allure
from pathlib import Path
from playwright.sync_api import Playwright, Page

# Đường dẫn lưu trữ trạng thái đăng nhập
BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_STATE_DIR = BASE_DIR / "reports" / "state"
AUTH_STATE_FILE = AUTH_STATE_DIR / "auth_state.json"


# 1. HOOK TỰ ĐỘNG TẠO SESSION TRƯỚC TOÀN BỘ TEST SUITE
def pytest_sessionstart(session):
    """Khởi tạo session đăng nhập một lần trước khi bắt đầu kiểm thử."""
    print("\n[HOOK] Đang khởi tạo phiên đăng nhập (Storage State)...")
    from playwright.sync_api import sync_playwright
    from pages.login_page import LoginPage

    AUTH_STATE_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        # Tự động headless trên CI/Ubuntu
        is_ci = os.getenv("CI", "false").lower() == "true"
        browser = p.chromium.launch(headless=is_ci)
        context = browser.new_context()
        page = context.new_page()

        login_page = LoginPage(page)
        login_page.open_url("https://www.saucedemo.com/")
        login_page.login("standard_user", "secret_sauce")
        page.locator(".inventory_list").wait_for(state="visible", timeout=10000)

        context.storage_state(path=str(AUTH_STATE_FILE))
        browser.close()
    print("[HOOK] Khởi tạo Storage State thành công!\n")


# 2. HOOK BẮT TRẠNG THÁI TEST (PASS / FAIL) ĐỂ BÁO CHO FIXTURE BIẾT
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook ghi nhận kết quả từng bước (setup, call, teardown) của test case."""
    outcome = yield
    report = outcome.get_result()
    # Gán kết quả thực thi vào item để fixture truy xuất
    setattr(item, f"rep_{report.when}", report)


# 3. FIXTURE QUẢN LÝ TRÌNH DUYỆT VÀ CHỤP ẢNH / QUAY VIDEO KHI FAIL
@pytest.fixture
def page(playwright: Playwright, request) -> Page:
    """Fixture tạo Page mới kèm tính năng tự động ghi hình và chụp ảnh khi lỗi."""
    is_ci = os.getenv("CI", "false").lower() == "true"
    browser = playwright.chromium.launch(headless=is_ci)
    
    # Kích hoạt ghi lại video màn hình vào thư mục tạm
    video_dir = BASE_DIR / "reports" / "videos"
    video_dir.mkdir(parents=True, exist_ok=True)
    
    context = browser.new_context(
        record_video_dir=str(video_dir),
        record_video_size={"width": 1280, "height": 720}
    )
    page_instance = context.new_page()

    yield page_instance

    # Sau khi test case chạy xong (Teardown phase):
    # Kiểm tra xem bài test có bị FAILED ở bước thực thi chính ("call") hay không
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        # A. Tự động chụp ảnh màn hình thời điểm lỗi
        screenshot_bytes = page_instance.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=f"FAILED_SCREENSHOT_{request.node.name}",
            attachment_type=allure.attachment_type.PNG
        )

    # Đóng page và context để Playwright flush file video ra đĩa
    page_instance.close()
    video_path = page_instance.video.path() if page_instance.video else None
    context.close()
    browser.close()

    # B. Nếu test fail, đính kèm luôn video quá trình chạy vào Allure
    if failed and video_path and os.path.exists(video_path):
        with open(video_path, "rb") as v_file:
            allure.attach(
                v_file.read(),
                name=f"FAILED_EXECUTION_VIDEO_{request.node.name}",
                attachment_type=allure.attachment_type.WEBM
            )
        # Xóa file video sau khi đã attach vào Allure để tránh nặng ổ đĩa
        try:
            os.remove(video_path)
        except OSError:
            pass
    elif video_path and os.path.exists(video_path):
        # Nếu test PASS, xóa file video thừa đi để tiết kiệm bộ nhớ
        try:
            os.remove(video_path)
        except OSError:
            pass


# 4. FIXTURE TRANG ĐÃ ĐƯỢC ĐĂNG NHẬP (SỬ DỤNG LẠI CHO CÁC BÀI TEST NGHIỆP VỤ)
@pytest.fixture
def authenticated_page(playwright: Playwright, request) -> Page:
    """Fixture tạo Page sử dụng sẵn session đăng nhập từ auth_state.json."""
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

    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if failed:
        screenshot_bytes = page_instance.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=f"FAILED_SCREENSHOT_{request.node.name}",
            attachment_type=allure.attachment_type.PNG
        )

    page_instance.close()
    video_path = page_instance.video.path() if page_instance.video else None
    context.close()
    browser.close()

    if failed and video_path and os.path.exists(video_path):
        with open(video_path, "rb") as v_file:
            allure.attach(
                v_file.read(),
                name=f"FAILED_EXECUTION_VIDEO_{request.node.name}",
                attachment_type=allure.attachment_type.WEBM
            )
        try:
            os.remove(video_path)
        except OSError:
            pass
    elif video_path and os.path.exists(video_path):
        try:
            os.remove(video_path)
        except OSError:
            pass