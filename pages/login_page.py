from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Quản lý locator tập trung
        self.username_input = self.page.locator("#user-name")
        self.password_input = self.page.locator("#password")
        self.login_btn = self.page.locator("#login-button")
        self.error_box = self.page.locator("[data-test='error']")

    def login(self, username: str, password: str):
        self.send_keys(self.username_input, username)
        self.send_keys(self.password_input, password)
        self.click(self.login_btn)

    def get_error_message(self) -> str:
        return self.get_text(self.error_box)