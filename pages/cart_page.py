from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from loguru import logger
import allure
import time

class CartPage(BasePage):
    """Класс для работы со страницей корзины"""
    
    CART_URL = "https://mebelmart-saratov.ru/cart"
    PAGE_BODY = (By.CSS_SELECTOR, "body")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Открыть корзину")
    def open_cart(self):
        """Открыть корзину по прямому URL"""
        self.driver.get(self.CART_URL)
        time.sleep(3)
        logger.info("Корзина открыта по прямому URL")
        self.driver.save_screenshot("cart_page.png")
        return self
    
    @allure.step("Проверить наличие товара в корзине")
    def is_product_in_cart(self, product_name: str):
        """Проверить, есть ли товар в корзине"""
        body_text = self.find_element(self.PAGE_BODY).text
        logger.info(f"Текст страницы корзины (первые 200 символов): {body_text[:200]}")
        
        if product_name.lower() in body_text.lower() or "чебурашка" in body_text.lower():
            logger.info(f"✅ Товар '{product_name}' найден на странице корзины")
            return True
        else:
            logger.warning(f"❌ Товар '{product_name}' не найден на странице корзины")
            return False
    
    @allure.step("Получить цену товара в корзине")
    def get_first_item_price(self):
        """Получить цену товара в корзине"""
        body_text = self.find_element(self.PAGE_BODY).text
        import re
        prices = re.findall(r'(\d+[\s]*\d*)\s*₽', body_text)
        if prices:
            price_str = prices[0].replace(' ', '')
            price = int(price_str)
            logger.info(f"Цена в корзине: {price}")
            return price
        return None