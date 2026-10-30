# pages/cart_page.py
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.backpack_add_btn = self.page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
        self.bike_light_add_btn = self.page.locator("[data-test='add-to-cart-sauce-labs-bike-light']")
        self.cart_badge = self.page.locator(".shopping_cart_badge")
        self.cart_icon = self.page.locator(".shopping_cart_link")

    def add_backpack_to_cart(self):
        self.click(self.backpack_add_btn)

    def add_bike_light_to_cart(self):
        self.click(self.bike_light_add_btn)

    def get_cart_badge_count(self) -> str:
        return self.get_text(self.cart_badge)

    def open_cart(self):
        self.click(self.cart_icon)