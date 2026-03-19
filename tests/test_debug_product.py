import allure
import pytest
from selenium.webdriver.common.by import By  # <-- ДОБАВЬ ЭТУ СТРОКУ
from pages.catalog_page import CatalogPage
import time

@allure.feature("Отладка")
class TestDebugProduct:
    
    def test_debug_product_page(self, driver):
        # Открыть раздел "Диваны"
        catalog_page = CatalogPage(driver)
        catalog_page.open_catalog()
        
        # Закрыть cookie баннер
        catalog_page.close_cookie_banner()
        
        # Кликнуть на первый товар
        products = catalog_page.get_all_products()
        if products:
            title_elem = products[0].find_element(By.CSS_SELECTOR, ".product-card__name a")
            product_name = title_elem.text
            title_elem.click()
            print(f"\nПерешли на страницу товара: {product_name}")
            time.sleep(3)
            
            # Сохраняем скриншот страницы товара
            driver.save_screenshot("product_page.png")
            print("Скриншот сохранен в product_page.png")
            
            # Сохраняем HTML страницы
            with open("product_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("HTML сохранен в product_page.html")
            
            # Ищем все ссылки и кнопки
            links = driver.find_elements(By.TAG_NAME, "a")
            print("\nВсе ссылки на странице:")
            for link in links:
                if link.text and ("купить" in link.text.lower() or "корзин" in link.text.lower()):
                    print(f"  - {link.text}: href={link.get_attribute('href')}")
            
            buttons = driver.find_elements(By.TAG_NAME, "button")
            print("\nВсе кнопки на странице:")
            for button in buttons:
                if button.text:
                    print(f"  - {button.text}")