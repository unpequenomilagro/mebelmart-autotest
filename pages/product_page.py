from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from loguru import logger
import allure
import time

class ProductPage(BasePage):
    """Класс для работы со страницей товара"""
    
    # Локаторы
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-card__now_price b")
    
    # Точный локатор для кнопки "В корзину" (найденный в HTML)
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "a.btnToCart.btn.btn-primary")
    # Альтернативный по классу
    ADD_TO_CART_BTN_CLASS = (By.CSS_SELECTOR, ".btnToCart")
    # По атрибуту data-price (с ценой товара)
    ADD_TO_CART_BTN_DATA = (By.CSS_SELECTOR, "a[data-price]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Проверить, что открыта страница товара")
    def verify_product_page(self, expected_name: str):
        """Проверить, что открыта страница нужного товара"""
        time.sleep(2)
        title = self.get_text(self.PRODUCT_TITLE)
        assert expected_name.lower() in title.lower(), \
            f"Ожидался товар '{expected_name}', открыт '{title}'"
        logger.info(f"Страница товара '{expected_name}' открыта корректно")
        return self
    
    @allure.step("Получить цену товара")
    def get_product_price(self):
        """Получить цену товара на странице"""
        try:
            # Цена также есть в data-price атрибуте кнопки
            cart_btn = self.find_element(self.ADD_TO_CART_BTN_DATA, timeout=5)
            price = int(cart_btn.get_attribute("data-price"))
            logger.info(f"Цена товара из data-price: {price}")
            return price
        except:
            try:
                price_text = self.get_text(self.PRODUCT_PRICE)
                import re
                numbers = re.findall(r'\d+', price_text)
                if numbers:
                    price = int(''.join(numbers))
                    logger.info(f"Цена товара на странице: {price}")
                    return price
            except Exception as e:
                logger.warning(f"Не удалось получить цену товара: {e}")
        return None
    
    @allure.step("Добавить товар в корзину")
    def add_to_cart(self):
        """Добавить товар в корзину через точную кнопку"""
        try:
            # Сохраняем скриншот перед добавлением
            self.driver.save_screenshot("before_add_to_cart.png")
            
            # Ищем кнопку "В корзину" по точному классу
            cart_btns = self.driver.find_elements(By.CSS_SELECTOR, "a.btnToCart.btn.btn-primary")
            
            if cart_btns:
                cart_btn = cart_btns[0]
                # Прокручиваем к элементу
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_btn)
                time.sleep(1)
                
                # Получаем цену из data-price для проверки
                price = cart_btn.get_attribute("data-price")
                logger.info(f"Добавляем товар с ценой: {price}")
                
                # Кликаем на кнопку
                cart_btn.click()
                logger.info("✅ Клик на кнопку 'В корзину'")
                time.sleep(3)
                
                # Проверяем, появился ли alert
                self.handle_cart_alert()
                return self
            else:
                # Пробуем другие варианты
                cart_btns = self.driver.find_elements(By.CSS_SELECTOR, ".btnToCart")
                if cart_btns:
                    cart_btns[0].click()
                    logger.info("✅ Клик на кнопку по классу .btnToCart")
                    time.sleep(3)
                    self.handle_cart_alert()
                    return self
                else:
                    logger.error("❌ Кнопка 'В корзину' не найдена")
                    self.driver.save_screenshot("no_cart_button.png")
        except Exception as e:
            logger.error(f"❌ Ошибка при добавлении в корзину: {e}")
            self.driver.save_screenshot("add_to_cart_error.png")
        return self
    
    @allure.step("Обработать alert корзины")
    def handle_cart_alert(self):
        """Обработать alert с предложением перейти в корзину"""
        try:
            time.sleep(2)
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            logger.info(f"Получен alert: {alert_text}")
            alert.accept()
            logger.info("Alert принят")
            time.sleep(2)
        except:
            logger.debug("Нет alert")