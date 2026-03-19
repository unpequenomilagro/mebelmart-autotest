from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
from loguru import logger
import allure
import time

class CatalogPage(BasePage):
    """Класс для работы со страницей каталога"""
    
    # Правильные локаторы на основе HTML
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-card")
    PRODUCT_TITLE = (By.CSS_SELECTOR, ".product-card__name a")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-card__now_price span b")
    PRODUCT_PRICE_FULL = (By.CSS_SELECTOR, ".product-card__now_price")
    ADD_TO_FAVORITE_BTN = (By.CSS_SELECTOR, ".favorite-icon")
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card")
    
    # Локаторы для фильтрации
    FILTER_PRICE_SLIDER = (By.ID, "w0")
    FILTER_PRICE_MIN = (By.CSS_SELECTOR, ".range-slider__down")
    FILTER_PRICE_MAX = (By.CSS_SELECTOR, ".range-slider__up")
    FILTER_APPLY_BTN = (By.CSS_SELECTOR, "#filterLinkContainer")
    
    # Локаторы для поиска
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.searchInput")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.submit")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Открыть страницу каталога")
    def open_catalog(self):
        """Открыть раздел Диваны"""
        logger.info(f"Открываем страницу: {Config.CATALOG_URL}")
        self.open(Config.CATALOG_URL)
        # Ждем загрузки товаров
        time.sleep(3)
        self.wait_for_products_load()
        logger.info("Каталог открыт")
        return self
    
    @allure.step("Ожидание загрузки товаров")
    def wait_for_products_load(self, timeout=30):
        """Ожидание загрузки товаров на странице"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PRODUCT_CARD)
            )
            logger.info("Товары загружены")
        except Exception as e:
            logger.error(f"Товары не загрузились: {e}")
            self.driver.save_screenshot("products_not_loaded.png")
            raise
    
    @allure.step("Получить список всех товаров")
    def get_all_products(self):
        """Получить список всех товаров на странице"""
        products = self.find_elements(self.PRODUCT_CARD)
        logger.info(f"Найдено товаров: {len(products)}")
        return products
    
    @allure.step("Получить название товара по индексу {index}")
    def get_product_name_by_index(self, index: int):
        """Получить название товара по индексу"""
        products = self.get_all_products()
        if 0 <= index < len(products):
            try:
                title_elem = products[index].find_element(*self.PRODUCT_TITLE)
                name = title_elem.text.strip()
                logger.info(f"Товар {index}: {name}")
                return name
            except:
                logger.warning(f"Не удалось получить название товара {index}")
                return None
        return None
    
    @allure.step("Получить цену товара по индексу {index}")
    def get_product_price_by_index(self, index: int):
        """Получить цену товара по индексу"""
        products = self.get_all_products()
        if 0 <= index < len(products):
            try:
                # Пробуем найти цену в разных местах
                price_elem = products[index].find_elements(By.CSS_SELECTOR, ".product-card__now_price span b")
                if price_elem:
                    price_text = price_elem[0].text.strip()
                else:
                    price_elem = products[index].find_elements(By.CSS_SELECTOR, ".product-card__now_price")
                    if price_elem:
                        price_text = price_elem[0].text.strip()
                    else:
                        return None
                
                # Извлекаем только цифры
                import re
                numbers = re.findall(r'\d+', price_text)
                if numbers:
                    price = int(''.join(numbers))
                    logger.info(f"Цена товара {index}: {price}")
                    return price
            except Exception as e:
                logger.warning(f"Не удалось получить цену товара {index}: {e}")
        return None
    
    @allure.step("Найти товар по названию: {product_name}")
    def find_product_by_name(self, product_name: str):
        """Найти товар по названию в каталоге"""
        products = self.get_all_products()
        for i, product in enumerate(products):
            try:
                title_elem = product.find_element(*self.PRODUCT_TITLE)
                if product_name.lower() in title_elem.text.lower():
                    logger.info(f"Найден товар '{product_name}' на позиции {i}")
                    return i, product
            except:
                continue
        logger.warning(f"Товар '{product_name}' не найден")
        return -1, None
    
    @allure.step("Нажать иконку избранного для первого товара")
    def add_first_product_to_favorites(self):
        """Добавить первый товар в избранное"""
        products = self.get_all_products()
        if products:
            try:
                fav_btn = products[0].find_element(*self.ADD_TO_FAVORITE_BTN)
                fav_btn.click()
                logger.info("Первый товар добавлен в избранное")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Не удалось добавить в избранное: {e}")
        return self
    
    @allure.step("Получить первый товар из категории Диваны")
    def get_first_sofa(self):
        """Получить первый товар, который действительно является диваном"""
        products = self.get_all_products()
        for i, product in enumerate(products):
            try:
                title_elem = product.find_element(*self.PRODUCT_TITLE)
                title = title_elem.text.lower()
                # Ищем ключевые слова, указывающие на диван
                if "диван" in title or "софа" in title or "кушетка" in title:
                    logger.info(f"Найден диван на позиции {i}: {title_elem.text}")
                    return i, product
            except:
                continue
        
        # Если не нашли диван, берем первый товар
        logger.warning("Диван не найден, берем первый товар")
        return 0, products[0] if products else None
    
    @allure.step("Получить название первого дивана")
    def get_first_sofa_name(self):
        """Получить название первого дивана в каталоге"""
        index, _ = self.get_first_sofa()
        return self.get_product_name_by_index(index)
    
    @allure.step("Получить цену первого дивана")
    def get_first_sofa_price(self):
        """Получить цену первого дивана в каталоге"""
        index, _ = self.get_first_sofa()
        return self.get_product_price_by_index(index)
    
    @allure.step("Добавить первый диван в корзину")
    def add_first_sofa_to_cart(self):
        """Добавить первый диван в корзину"""
        index, product = self.get_first_sofa()
        if product:
            try:
                # Запоминаем название товара
                product_name = self.get_product_name_by_index(index)
                
                # Кликаем на название товара
                title_elem = product.find_element(*self.PRODUCT_TITLE)
                title_elem.click()
                logger.info(f"Клик на диван '{product_name}' для перехода в карточку товара")
                time.sleep(3)
                
                # На странице товара ищем кнопку "Купить"
                from pages.product_page import ProductPage
                product_page = ProductPage(self.driver)
                
                # Проверяем, что мы на странице товара
                product_page.verify_product_page(product_name)
                
                # Добавляем в корзину
                product_page.add_to_cart()
                
                logger.info(f"Диван '{product_name}' добавлен в корзину")
                
            except Exception as e:
                logger.error(f"Не удалось добавить диван в корзину: {e}")
                self.driver.save_screenshot("add_to_cart_error.png")
        return self
    
    @allure.step("Нажать на товар по индексу {index}")
    def click_on_product_by_index(self, index: int):
        """Кликнуть на товар по индексу"""
        products = self.get_all_products()
        if 0 <= index < len(products):
            try:
                title_elem = products[index].find_element(*self.PRODUCT_TITLE)
                title_elem.click()
                logger.info(f"Клик на товар {index}")
                time.sleep(2)
            except Exception as e:
                logger.error(f"Не удалось кликнуть на товар: {e}")
                raise
        return self
    
    @allure.step("Получить название первого товара")
    def get_first_product_name(self):
        """Получить название первого товара в каталоге"""
        return self.get_product_name_by_index(0)
    
    @allure.step("Получить цену первого товара")
    def get_first_product_price(self):
        """Получить цену первого товара в каталоге"""
        return self.get_product_price_by_index(0)
    
    @allure.step("Применить фильтр по цене")
    def apply_price_filter(self, min_price=None, max_price=None):
        """Применить фильтр по цене"""
        if self.is_element_present(self.FILTER_APPLY_BTN):
            self.click(self.FILTER_APPLY_BTN)
            time.sleep(3)
            self.wait_for_products_load()
            logger.info("Фильтр применен")
        return self