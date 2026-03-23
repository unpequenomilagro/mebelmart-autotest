from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
from loguru import logger
import allure
import time

class CatalogPage(BasePage):
    """Страница каталога диванов"""
    
    # Локаторы
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-card__name a")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-card__now_price b")
    ADD_TO_FAVORITE = (By.CSS_SELECTOR, ".favorite-icon")
    FILTER_APPLY = (By.CSS_SELECTOR, "#filterLinkContainer")
    
    def open_catalog(self):
        """Открыть раздел Диваны"""
        self.open(Config.CATALOG_URL)
        time.sleep(2)
        self.wait_for_products_load(timeout=15)
        logger.info("Каталог открыт")
        return self
    
    def wait_for_products_load(self, timeout=15):
        """Ожидание загрузки товаров"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.PRODUCT_CARD)
        )
    
    def get_all_products(self):
        """Получить список всех товаров"""
        return self.find_elements(self.PRODUCT_CARD)
    
    def get_product_title_by_index(self, index):
        """Получить название товара по индексу"""
        products = self.get_all_products()
        if 0 <= index < len(products):
            return products[index].find_element(*self.PRODUCT_TITLE).text.strip()
        return None
    
    def get_product_price_by_index(self, index):
        """Получить цену товара по индексу"""
        products = self.get_all_products()
        if 0 <= index < len(products):
            try:
                price_text = products[index].find_element(*self.PRODUCT_PRICE).text
                import re
                price = re.sub(r'[^\d]', '', price_text)
                return int(price) if price else None
            except:
                return None
        return None
    
    def find_sofa_by_name(self, sofa_name):
        """Найти диван по названию, вернуть индекс и элемент"""
        products = self.get_all_products()
        for i, product in enumerate(products):
            try:
                title = product.find_element(*self.PRODUCT_TITLE).text.strip()
                if sofa_name.lower() in title.lower():
                    logger.info(f"Найден товар '{title}' на позиции {i}")
                    return i, product
            except:
                continue
        logger.warning(f"Товар '{sofa_name}' не найден")
        return -1, None
    
    def click_on_product(self, index):
        """Кликнуть на товар по индексу"""
        products = self.get_all_products()
        if 0 <= index < len(products):
            element = products[index].find_element(*self.PRODUCT_TITLE)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            self.wait_for_page_load()
            logger.info(f"Клик на товар {index}")
        return self
    
    def add_to_favorites(self, index=0):
        """Добавить товар в избранное"""
        products = self.get_all_products()
        if 0 <= index < len(products):
            element = products[index].find_element(*self.ADD_TO_FAVORITE)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            logger.info(f"Товар {index} добавлен в избранное")
        return self
    
    def apply_filter(self):
        """Применить фильтр"""
        self.click(self.FILTER_APPLY)
        time.sleep(2)
        self.wait_for_products_load(timeout=10)
        logger.info("Фильтр применен")
        return self
    
    def go_to_favorites(self):
        """Перейти в избранное"""
        self.driver.get(f"{Config.BASE_URL}/favorite/")
        self.wait_for_page_load()
        return self
    
    def go_to_cart(self):
        """Перейти в корзину"""
        self.driver.get(f"{Config.BASE_URL}/cart")
        self.wait_for_page_load()
        return self