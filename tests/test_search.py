import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
import time

@allure.feature("Поиск")
@allure.story("Поиск по названию")
class TestSearch:
    
    @allure.title("Поиск товара по названию")
    @allure.description("Тест проверяет, что поиск по названию работает корректно")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_name(self, driver):
        # Открыть страницу каталога диванов
        print("\n🔍 Открываем каталог диванов...")
        driver.get("https://mebelmart-saratov.ru/myagkaya_mebel_v_saratove/divanyi_v_saratove")
        time.sleep(3)
        
        # Закрыть cookie баннер
        try:
            cookie_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Принять')]")
            cookie_btn.click()
            print("🍪 Cookie баннер закрыт")
            time.sleep(1)
        except:
            print("Нет cookie баннера")
        
        # Найти поле поиска в каталоге
        print("🔎 Поиск поля для ввода...")
        try:
            # В каталоге есть поле поиска
            search_input = driver.find_element(By.CSS_SELECTOR, "input.searchInput")
            print("✅ Поле поиска найдено")
            
            # Прокрутить к полю
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_input)
            time.sleep(1)
            
            # Очистить поле через JavaScript
            driver.execute_script("arguments[0].value = '';", search_input)
            time.sleep(0.5)
            
            # Ввести запрос
            search_query = "ЧБ"
            print(f"📝 Вводим запрос: {search_query}")
            driver.execute_script(f"arguments[0].value = '{search_query}';", search_input)
            time.sleep(0.5)
            
            # Нажать Enter через JavaScript
            driver.execute_script("""
                var event = new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    which: 13,
                    keyCode: 13,
                    bubbles: true
                });
                arguments[0].dispatchEvent(event);
            """, search_input)
            print("⏎ Нажат Enter")
            
            time.sleep(3)
            
            # Проверить результаты - ищем диван ЧБ в результатах
            print("🔍 Проверяем результаты поиска...")
            
            # Сохраняем скриншот результатов
            driver.save_screenshot("search_results.png")
            print("📸 Скриншот результатов сохранен")
            
            # Ищем все товары на странице
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card")
            print(f"Найдено товаров в результатах: {len(products)}")
            
            found = False
            for i, product in enumerate(products):
                try:
                    title = product.find_element(By.CSS_SELECTOR, ".product-card__name a").text
                    print(f"{i}: {title}")
                    if "чб" in title.lower():
                        found = True
                        print(f"✅ Найден диван ЧБ: {title}")
                        break
                except:
                    continue
            
            assert found, "Диван ЧБ не найден в результатах поиска"
            print("✅ Тест успешно завершен!")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            # Сохраняем скриншот ошибки
            driver.save_screenshot("search_error.png")
            raise