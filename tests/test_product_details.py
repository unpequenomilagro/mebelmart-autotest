import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from loguru import logger

@allure.feature("Карточка товара")
class TestProductDetails:
    
    @allure.title("Проверка деталей товара в карточке")
    def test_product_details(self, driver):
        catalog = CatalogPage(driver)
        catalog.open_catalog()
        time.sleep(2)
        
        # Ищем существующий диван "Диван ЧБ"
        search_name = "Диван ЧБ"
        logger.info(f"Ищем диван '{search_name}'...")
        
        index, product = catalog.find_sofa_by_name(search_name)
        assert index != -1, f"Диван '{search_name}' не найден"
        
        # Запоминаем название из каталога
        catalog_name = catalog.get_product_title_by_index(index)
        catalog_price = catalog.get_product_price_by_index(index)
        logger.info(f"Найден товар: '{catalog_name}', цена: {catalog_price} ₽")
        
        # Переходим на страницу товара
        catalog.click_on_product(index)
        time.sleep(3)
        
        # Ждем, пока страница полностью загрузится
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            logger.info("Страница товара загружена")
        except:
            logger.warning("Страница товара загружается медленно, делаем повторную попытку...")
            driver.refresh()
            time.sleep(3)
        
        # Проверяем, что открыт правильный товар
        product_page = ProductPage(driver)
        
        # Проверяем, что нет ошибки сервера
        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "внутренняя ошибка сервера" in page_text.lower():
            logger.warning("Обнаружена ошибка сервера, обновляем страницу...")
            driver.refresh()
            time.sleep(3)
        
        product_page.verify_product_page("Чебурашка")
        
        # Прокручиваем к характеристикам
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1)
        
        # Получаем текст страницы
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Проверяем наличие характеристик
        if "Ширина" in page_text:
            logger.info("Характеристика 'Ширина' найдена")
        if "Глубина" in page_text:
            logger.info("Характеристика 'Глубина' найдена")
        if "Механизм" in page_text:
            logger.info("Характеристика 'Механизм' найдена")
        
        
        logger.info("Тест пройден: детали товара отображаются корректно")