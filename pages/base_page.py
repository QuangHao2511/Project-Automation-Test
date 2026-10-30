from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open_url(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def click(self, locator: Locator):
        locator.wait_for(state="visible")
        locator.click()

    def send_keys(self, locator: Locator, text: str):
        locator.wait_for(state="visible")
        locator.fill(text)

    def get_text(self, locator: Locator) -> str:
        locator.wait_for(state="visible")
        return locator.inner_text().strip()