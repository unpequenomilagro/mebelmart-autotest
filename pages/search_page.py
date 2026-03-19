from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from loguru import logger
import allure

class SearchPage(BasePage):
    """Класс для работы с поиском"""
    
    # Локаторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.search-btn")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search-results .product-item")
    SEARCH_RESULT_TITLE = (By.CSS_SELECTOR, ".product-title a")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".no-results-message")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    @allure.step("Выполнить поиск по запросу: {query}")
    def search(self, query: str):
        """Выполнить поиск по запросу"""
        search_input = self.find_element(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)
        logger.info(f"Выполнен поиск по запросу: '{query}'")
        # Ждем результаты поиска
        self.wait_for_element_visible(self.SEARCH_RESULTS)
        return self
    
    @allure.step("Получить названия результатов поиска")
    def get_search_results_titles(self):
        """Получить список названий товаров в результатах поиска"""
        titles = []
        elements = self.find_elements(self.SEARCH_RESULT_TITLE)
        for element in elements:
            titles.append(element.text)
        logger.info(f"Найдено результатов: {len(titles)}")
        return titles
    
    @allure.step("Проверить, что первый результат содержит '{expected_text}'")
    def verify_first_result_contains(self, expected_text: str):
        """Проверить, что первый результат поиска содержит ожидаемый текст"""
        titles = self.get_search_results_titles()
        if titles:
            first_result = titles[0]
            assert expected_text.lower() in first_result.lower(), \
                f"Первый результат '{first_result}' не содержит '{expected_text}'"
            logger.info(f"Первый результат содержит '{expected_text}'")
        else:
            raise AssertionError("Нет результатов поиска")
        return self