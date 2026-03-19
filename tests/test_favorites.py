import allure
import pytest
from selenium.webdriver.common.by import By
from pages.catalog_page import CatalogPage
from pages.favorites_page import FavoritesPage
import time

@allure.feature("Избранное")
@allure.story("Добавление в избранное")
class TestFavorites:
    
    @allure.title("Добавление товара в избранное")
    @allure.description("Тест проверяет добавление товара в избранное")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_to_favorites(self, driver):
        # Открыть раздел "Диваны"
        catalog_page = CatalogPage(driver)
        catalog_page.open_catalog()
        
        # Найти диван "Диван ЧБ"
        products = catalog_page.get_all_products()
        found_index = -1
        
        for i, product in enumerate(products):
            try:
                title_elem = product.find_element(By.CSS_SELECTOR, ".product-card__name a")
                title = title_elem.text.strip()
                if "чб" in title.lower():
                    found_index = i
                    product_name = title
                    break
            except:
                continue
        
        assert found_index != -1, "Диван ЧБ не найден в каталоге"
        print(f"Найден диван: {product_name}")
        
        # Добавить найденный диван в избранное
        favorites_btn = products[found_index].find_element(By.CSS_SELECTOR, ".favorite-icon")
        favorites_btn.click()
        print("Товар добавлен в избранное")
        time.sleep(2)
        
        # Перейти в избранное по прямому URL
        driver.get("https://mebelmart-saratov.ru/favorite/")
        time.sleep(3)
        
        # Проверить, что товар в избранном
        page_text = driver.find_element(By.TAG_NAME, "body").text
        assert "ЧБ" in page_text or "Чебурашка" in page_text, "Товар не найден в избранном"
        print("✅ Товар найден в избранном")