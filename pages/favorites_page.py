from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from loguru import logger
import allure

class FavoritesPage(BasePage):
    """Класс для работы со страницей избранного"""
    
    # Локаторы
    FAVORITE_ITEMS = (By.CSS_SELECTOR, ".favorite-item")
    FAVORITE_ITEM_TITLE = (By.CSS_SELECTOR, ".favorite-item-title")
    FAVORITE_ICON = (By.CSS_SELECTOR, ".favorite-icon")
    EMPTY_FAVORITES_MESSAGE = (By.CSS_SELECTOR, ".empty-favorites-message")
    FAVORITE_BTN_ACTIVE = (By.CSS_SELECTOR, ".favorite-btn.active")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Открыть избранное")
    def open_favorites(self):
        """Открыть страницу избранного через иконку"""
        self.click(self.FAVORITE_ICON)
        logger.info("Страница избранного открыта")
        return self
    
    @allure.step("Проверить наличие товара в избранном")
    def is_product_in_favorites(self, product_name: str):
        """Проверить, есть ли товар в избранном"""
        items = self.find_elements(self.FAVORITE_ITEM_TITLE)
        for item in items:
            if product_name.lower() in item.text.lower():
                logger.info(f"Товар '{product_name}' найден в избранном")
                return True
        logger.warning(f"Товар '{product_name}' не найден в избранном")
        return False
    
    @allure.step("Проверить, что иконка избранного активна")
    def is_favorite_icon_active(self):
        """Проверить, активна ли иконка избранного (закрашена)"""
        return self.is_element_present(self.FAVORITE_BTN_ACTIVE)