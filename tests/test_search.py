import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
from loguru import logger

@allure.feature("Поиск")
class TestSearch:
    
    @allure.title("Поиск товара по названию")
    def test_search_by_name(self, driver):
        # 1. Открываем главную страницу
        driver.get(Config.BASE_URL)
        time.sleep(2)
        
        # 2. Закрываем cookie баннер
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Принять')]"))
            )
            cookie_btn.click()
            logger.info("Cookie баннер закрыт")
            time.sleep(1)
        except:
            logger.info("Cookie баннер не найден")
        
        # 3. Находим поле поиска в верхней части страницы
        try:
            # Ищем видимое поле поиска (не скрытое)
            search_inputs = driver.find_elements(By.CSS_SELECTOR, "input.searchInput")
            search_input = None
            for inp in search_inputs:
                if inp.is_displayed() and inp.is_enabled():
                    search_input = inp
                    break
            
            if not search_input:
                # Если не нашли, пробуем другой селектор
                search_input = driver.find_element(By.CSS_SELECTOR, "input[name='query']")
            
            logger.info("Найдено поле поиска")
            
            # 4. Прокручиваем к полю поиска
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_input)
            time.sleep(1)
            
            # 5. Кликаем для активации
            search_input.click()
            time.sleep(0.5)
            
            # 6. Вводим запрос
            search_query = "Бостон"
            logger.info(f"Вводим запрос: '{search_query}'")
            search_input.clear()
            search_input.send_keys(search_query)
            time.sleep(0.5)
            
            # 7. Нажимаем Enter
            search_input.send_keys(Keys.RETURN)
            logger.info("⏎ Нажат Enter")
            time.sleep(3)
            
            
            # 8. Проверяем результаты
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-card"))
            )
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            logger.info(f"Найдено товаров в результатах: {len(products)}")
            
            assert len(products) > 0, "Нет результатов поиска"
            
            # 9. Проверяем первый товар
            first_title = products[0].find_element(By.CSS_SELECTOR, ".product-card__name a").text
            logger.info(f"Первый товар: '{first_title}'")
            
            assert "Бостон" in first_title, f"Первый товар не содержит 'Бостон'"
            logger.info("Тест пройден: поиск работает корректно")
            
        except Exception as e:
            logger.error(f"Ошибка при поиске: {e}")
            driver.save_screenshot("search_error.png")
            raise