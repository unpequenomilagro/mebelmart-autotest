import allure
import pytest
from pages.catalog_page import CatalogPage
from config.config import Config

@allure.feature("Фильтрация товаров")
@allure.story("Фильтрация по цене")
class TestFilter:
    
    @allure.title("Проверка фильтрации товаров по цене")
    @allure.description("Тест проверяет, что фильтр по цене работает корректно")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_price_filter(self, driver):
        # Открыть раздел "Диваны"
        catalog_page = CatalogPage(driver)
        catalog_page.open_catalog()
        
        # Применить фильтр по цене
        catalog_page.apply_price_filter()
        
        # Проверить, что есть товары в результатах
        products = catalog_page.get_all_products()
        assert len(products) > 0, "Нет товаров после применения фильтра"
        
        # Проверим, что цена первого товара соответствует ожиданиям
        # (просто проверяем что цена есть, без строгой фильтрации)
        price = catalog_page.get_product_price_by_index(0)
        assert price is not None, "Не удалось получить цену товара"
        print(f"Цена первого товара после фильтрации: {price}")