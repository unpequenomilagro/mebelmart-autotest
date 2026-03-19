import allure
import pytest
from selenium.webdriver.common.by import By
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
import time

@allure.feature("Карточка товара")
@allure.story("Детали товара")
class TestProductDetails:
    
    @allure.title("Проверка деталей товара в карточке")
    @allure.description("Тест проверяет, что в карточке товара отображаются корректные характеристики")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_details(self, driver):
        # Открыть раздел "Диваны"
        catalog_page = CatalogPage(driver)
        catalog_page.open_catalog()
        
        # Найти конкретный диван "Диван ЧБ"
        print("\n🔍 Поиск дивана ЧБ в каталоге...")
        products = catalog_page.get_all_products()
        found_index = -1
        product_name = ""
        
        for i, product in enumerate(products):
            try:
                title_elem = product.find_element(By.CSS_SELECTOR, ".product-card__name a")
                title = title_elem.text.strip()
                print(f"{i}: {title}")
                if "чб" in title.lower():
                    found_index = i
                    product_name = title
                    print(f"✅ Найден диван на позиции {i}: {title}")
                    break
            except Exception as e:
                print(f"{i}: Ошибка - {e}")
        
        assert found_index != -1, "Диван ЧБ не найден в каталоге"
        
        # Кликнуть на товар
        print(f"➡️ Переход на страницу дивана: {product_name}")
        title_elem = products[found_index].find_element(By.CSS_SELECTOR, ".product-card__name a")
        title_elem.click()
        time.sleep(3)
        
        # Проверить, что открылась страница правильного товара
        product_page = ProductPage(driver)
        page_title = product_page.get_text(product_page.PRODUCT_TITLE)
        print(f"Заголовок страницы: {page_title}")
        assert "Чебурашка" in page_title or "ЧБ" in page_title, "Открыта не та страница товара"
        
        # Проверить наличие цены
        price = product_page.get_product_price()
        assert price is not None, "Цена товара не найдена"
        assert price > 0, "Цена должна быть положительным числом"
        print(f"💰 Цена товара: {price}")
        
        # Проверить наличие характеристик (ищем на странице)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        print("🔍 Проверяем наличие характеристик...")
        
        # Характеристики, которые должны быть на странице
        characteristics = ["Ширина", "Глубина", "Механизм"]
        found_chars = []
        
        for char in characteristics:
            if char in page_text:
                found_chars.append(char)
                print(f"✅ Найдена характеристика: {char}")
        
        assert len(found_chars) > 0, "Характеристики не найдены на странице"
        print(f"✅ Найдено характеристик: {len(found_chars)}")