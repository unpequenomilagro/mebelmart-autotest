from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from loguru import logger
import allure

class FavoritesPage(BasePage):
    """Страница избранного"""
    
    def is_product_in_favorites(self, product_name):
        """Проверить наличие товара в избранном"""
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        result = product_name.lower() in page_text.lower()
        if result:
            logger.info(f"✅ Товар '{product_name}' найден в избранном")
        else:
            logger.warning(f"❌ Товар '{product_name}' не найден в избранном")
        return result