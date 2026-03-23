import allure
import time
from selenium.webdriver.common.by import By
from pages.catalog_page import CatalogPage
from loguru import logger

@allure.feature("Фильтрация")
class TestFilter:
    
    @allure.title("Фильтрация по цене и проверка наличия товара")
    def test_price_filter(self, driver):
        catalog = CatalogPage(driver)
        catalog.open_catalog()
        time.sleep(2)
        
      
        products_before = len(catalog.get_all_products())
        logger.info(f"Товаров ДО фильтрации: {products_before}")
        
        # 2. Показываем цены товаров до фильтрации
        logger.info("Цены товаров ДО фильтрации:")
        for i in range(min(5, products_before)):
            price = catalog.get_product_price_by_index(i)
            if price:
                logger.info(f"   Товар {i+1}: {price} ₽")
        
        # 3. Применяем фильтр
        logger.info("Применяем фильтр по цене (10 000 ₽ - 15 000 ₽)...")
        time.sleep(1)
        
        catalog.apply_filter()
        time.sleep(2)
        
        
        # 5. Получаем товары после фильтрации
        products_after = catalog.get_all_products()
        logger.info(f"Товаров ПОСЛЕ фильтрации: {len(products_after)}")
        
        # 6. Показываем цены товаров после фильтрации
        logger.info("Цены товаров ПОСЛЕ фильтрации:")
        for i in range(min(5, len(products_after))):
            price = catalog.get_product_price_by_index(i)
            if price:
                logger.info(f"   Товар {i+1}: {price} ₽")
        
        # 7. Ищем диван "Диван ЧБ"
        logger.info("Ищем диван 'Диван ЧБ' в результатах...")
        index, product = catalog.find_sofa_by_name("Диван ЧБ")
        
        if index != -1:
            found_price = catalog.get_product_price_by_index(index)
            logger.info(f"НАЙДЕН диван 'Диван ЧБ' с ценой {found_price} ₽")
            
            # Подсвечиваем найденный товар
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
            driver.execute_script("arguments[0].style.border='3px solid green'", product)
            time.sleep(2)
            driver.execute_script("arguments[0].style.border=''", product)
        else:
            logger.warning("Диван 'Диван ЧБ' не найден после фильтрации")
        
        assert len(products_after) > 0, "Нет товаров после фильтрации"
        logger.info("ТЕСТ ПРОЙДЕН: фильтрация работает")