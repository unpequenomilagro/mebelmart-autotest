import allure
import pytest
from selenium.webdriver.common.by import By
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
import time

@allure.feature("Корзина")
@allure.story("Добавление конкретного дивана")
class TestCart:
    
    @allure.title("Добавление дивана 'ЧБ' в корзину и проверка цены")
    @allure.description("Тест находит диван ЧБ в каталоге, добавляет в корзину и проверяет цену")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_specific_sofa_to_cart(self, driver):
        # 1. Открыть раздел "Диваны"
        catalog_page = CatalogPage(driver)
        catalog_page.open_catalog()
        
        # 2. Закрыть cookie баннер
        catalog_page.close_cookie_banner()
        
        # 3. Ищем диван "Диван ЧБ"
        target_sofa_name = "Диван ЧБ"
        print(f"\n🔍 Ищем диван: '{target_sofa_name}'")
        
        products = catalog_page.get_all_products()
        found_index = -1
        found_title = ""
        
        for i, product in enumerate(products):
            try:
                title_elem = product.find_element(By.CSS_SELECTOR, ".product-card__name a")
                title = title_elem.text.strip()
                print(f"{i}: {title}")
                
                if "чб" in title.lower():
                    print(f"  ✅ НАЙДЕН на позиции {i}: {title}")
                    found_index = i
                    found_title = title
                    break
            except Exception as e:
                print(f"{i}: Ошибка - {e}")
        
        assert found_index != -1, f"Диван '{target_sofa_name}' не найден"
        print(f"\n✅ Выбран диван: {found_title}")
        
        # 4. Запомнить цену
        sofa_price = catalog_page.get_product_price_by_index(found_index)
        assert sofa_price is not None, "Не удалось получить цену дивана"
        print(f"💰 Цена дивана: {sofa_price}")
        
        # 5. Перейти на страницу дивана
        title_elem = products[found_index].find_element(By.CSS_SELECTOR, ".product-card__name a")
        title_elem.click()
        print("➡️ Переход на страницу дивана...")
        time.sleep(3)
        
        # 6. Добавить в корзину через кнопку "КУПИТЬ В 1 КЛИК"
        product_page = ProductPage(driver)
        product_page.add_to_cart()
        print("🛒 Товар добавлен в корзину")
        
        # 7. Перейти в корзину
        cart_page = CartPage(driver)
        cart_page.open_cart()
        print("📦 Открыта корзина")
        
        # 8. Проверить, что товар в корзине
        time.sleep(2)
        in_cart = cart_page.is_product_in_cart("ЧБ")
        print(f"Результат проверки корзины: {in_cart}")
        
        assert in_cart, f"Диван 'ЧБ' не найден в корзине"
        
        print("✅ Тест успешно завершен!")