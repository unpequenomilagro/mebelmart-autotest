from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
import allure
import time

class ProductPage(BasePage):
    """Страница товара"""
    
    # Локаторы
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-card__now_price b")
    ADD_TO_CART = (By.XPATH, "//a[contains(text(), 'В КОРЗИНУ')]")
    ADD_TO_CART_ALT = (By.CSS_SELECTOR, "a.btnToCart")
    BUY_BUTTON = (By.XPATH, "//button[contains(text(), 'КУПИТЬ В 1 КЛИК')]")
    
    def verify_product_page(self, expected_name):
        """Проверить, что открыта страница товара (по части названия)"""
        try:
            # Ждем, пока заголовок появится
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PRODUCT_TITLE)
            )
            title = self.get_text(self.PRODUCT_TITLE)
            
            # Проверяем, что это не ошибка сервера
            if "внутренняя ошибка сервера" in title.lower():
                logger.warning("Обнаружена ошибка сервера, обновляем страницу...")
                self.driver.refresh()
                time.sleep(2)
                title = self.get_text(self.PRODUCT_TITLE)
            
            assert expected_name.lower() in title.lower(), f"Ожидалось название, содержащее '{expected_name}', получено '{title}'"
            logger.info(f"Страница товара с '{expected_name}' открыта")
        except Exception as e:
            logger.error(f"Ошибка при проверке страницы товара: {e}")
            self.driver.save_screenshot("product_page_error.png")
            raise
        return self
    
    def get_product_price(self):
        """Получить цену товара"""
        try:
            price_text = self.get_text(self.PRODUCT_PRICE)
            import re
            price = re.sub(r'[^\d]', '', price_text)
            return int(price) if price else None
        except:
            return None
    
    def add_to_cart(self):
        """Добавить товар в корзину"""
        # Пробуем разные локаторы
        for locator in [self.ADD_TO_CART, self.ADD_TO_CART_ALT, self.BUY_BUTTON]:
            try:
                element = self.wait_for_element_clickable(locator, timeout=5)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element.click()
                logger.info("Товар добавлен в корзину")
                break
            except:
                continue
        else:
            raise Exception("Кнопка 'В корзину' не найдена")
        
        # Обработка alert
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            logger.info("Alert принят")
        except:
            pass
        return self