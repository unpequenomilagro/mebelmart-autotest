from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config.config import Config
from loguru import logger
import allure
import time

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
    
    def open(self, url):
        """Открыть страницу"""
        logger.info(f"Открываем: {url}")
        with allure.step(f"Открыть {url}"):
            self.driver.get(url)
            self.wait_for_page_load()
            self.close_cookie_banner()
    
    def wait_for_page_load(self, timeout=10):
        """Ожидание загрузки страницы"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    
    def close_cookie_banner(self):
        """Закрыть баннер с cookies"""
        try:
            cookie_btn = (By.XPATH, "//button[contains(text(), 'Принять')]")
            if self.is_element_present(cookie_btn, timeout=2):
                self.click(cookie_btn)
                logger.info("Cookie баннер закрыт")
        except:
            pass
    
    def wait_for_element_clickable(self, locator, timeout=Config.EXPLICIT_WAIT):
        """Ожидать, пока элемент станет кликабельным"""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
    
    def click(self, locator, timeout=Config.EXPLICIT_WAIT):
        """Кликнуть на элемент"""
        element = self.wait_for_element_clickable(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()
        logger.info(f"Клик: {locator}")
    
    def find_element(self, locator, timeout=Config.EXPLICIT_WAIT):
        """Найти элемент"""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator, timeout=Config.EXPLICIT_WAIT):
        """Найти все элементы"""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
    
    def get_text(self, locator):
        """Получить текст элемента"""
        return self.find_element(locator).text
    
    def is_element_present(self, locator, timeout=2):
        """Проверить наличие элемента"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False