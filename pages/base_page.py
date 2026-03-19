from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config
from utils.allure_helper import AllureHelper
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
        logger.info(f"Открываем страницу: {url}")
        with allure.step(f"Открыть страницу: {url}"):
            self.driver.get(url)
            self.close_cookie_banner()
    
    @allure.step("Закрыть баннер с cookies")
    def close_cookie_banner(self):
        """Закрыть баннер с cookies, если он появился"""
        try:
            cookie_accept_btn = (By.XPATH, "//button[contains(text(), 'Принять') or contains(text(), 'Согласен')]")
            if self.is_element_present(cookie_accept_btn, timeout=2):
                self.click(cookie_accept_btn)
                logger.info("Cookie баннер закрыт")
                time.sleep(0.5)
                return True
        except Exception as e:
            logger.debug(f"Не удалось закрыть cookie баннер: {e}")
        return False
    
    def find_element(self, locator: tuple, timeout=Config.EXPLICIT_WAIT):
        """Найти элемент с явным ожиданием"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Элемент не найден: {locator}")
            AllureHelper.attach_screenshot(self.driver, "Ошибка_поиска_элемента")
            raise
    
    def find_elements(self, locator: tuple, timeout=Config.EXPLICIT_WAIT):
        """Найти все элементы по локатору"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            logger.error(f"Элементы не найдены: {locator}")
            return []
    
    def click(self, locator: tuple, timeout=Config.EXPLICIT_WAIT):
        """Кликнуть на элемент"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.3)
            element.click()
            logger.info(f"Клик на элемент: {locator}")
        except Exception as e:
            logger.error(f"Не удалось кликнуть на элемент {locator}: {e}")
            AllureHelper.attach_screenshot(self.driver, "Ошибка_клика")
            raise
    
    def input_text(self, locator: tuple, text: str, timeout=Config.EXPLICIT_WAIT):
        """Ввести текст в поле"""
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
            logger.info(f"Ввод текста '{text}' в поле: {locator}")
        except Exception as e:
            logger.error(f"Не удалось ввести текст: {e}")
            AllureHelper.attach_screenshot(self.driver, "Ошибка_ввода_текста")
            raise
    
    def get_text(self, locator: tuple, timeout=Config.EXPLICIT_WAIT):
        """Получить текст элемента"""
        element = self.find_element(locator, timeout)
        text = element.text
        logger.info(f"Получен текст из {locator}: {text}")
        return text
    
    def is_element_present(self, locator: tuple, timeout=5):
        """Проверить наличие элемента на странице"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False
    
    def wait_for_element_visible(self, locator: tuple, timeout=Config.EXPLICIT_WAIT):
        """Ожидать видимости элемента"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f"Элемент видим: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Элемент не стал видимым: {locator}")
            AllureHelper.attach_screenshot(self.driver, "Ошибка_видимости")
            raise