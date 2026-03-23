from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from loguru import logger
import allure

class CartPage(BasePage):
    """Страница корзины"""
    
    def is_product_in_cart(self, product_name):
        """Проверить наличие товара в корзине"""
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        result = product_name.lower() in page_text.lower()
        if result:
            logger.info(f"✅ Товар '{product_name}' найден в корзине")
        else:
            logger.warning(f"❌ Товар '{product_name}' не найден в корзине")
        return result