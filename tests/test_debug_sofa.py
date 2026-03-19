import allure
import pytest
from selenium.webdriver.common.by import By
from pages.catalog_page import CatalogPage
import time

@allure.feature("Отладка")
class TestDebugSofaPage:
    
    def test_debug_sofa_page(self, driver):
        # 1. Открыть раздел "Диваны"
        catalog_page = CatalogPage(driver)
        catalog_page.open_catalog()
        
        # 2. Закрыть cookie баннер
        catalog_page.close_cookie_banner()
        
        # 3. Найти диван "Диван ЧБ"
        products = catalog_page.get_all_products()
        for i, product in enumerate(products):
            try:
                title_elem = product.find_element(By.CSS_SELECTOR, ".product-card__name a")
                title = title_elem.text.strip()
                if "чб" in title.lower():
                    print(f"\n✅ Найден диван ЧБ на позиции {i}")
                    # 4. Перейти на страницу дивана
                    title_elem.click()
                    time.sleep(3)
                    break
            except:
                continue
        
        # 5. Сохраняем скриншот страницы товара
        driver.save_screenshot("sofa_page.png")
        print("📸 Скриншот сохранен: sofa_page.png")
        
        # 6. Сохраняем HTML страницы
        with open("sofa_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 HTML сохранен: sofa_page.html")
        
        # 7. Ищем все ссылки и кнопки, связанные с корзиной
        print("\n=== ПОИСК ЭЛЕМЕНТОВ ДЛЯ ДОБАВЛЕНИЯ В КОРЗИНУ ===")
        
        # Ищем ссылки с текстом
        links = driver.find_elements(By.TAG_NAME, "a")
        print("\nСсылки:")
        for link in links:
            text = link.text.strip()
            href = link.get_attribute('href')
            if text and ("корзин" in text.lower() or "купить" in text.lower() or "добав" in text.lower()):
                print(f"  - '{text}' -> {href}")
        
        # Ищем кнопки
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print("\nКнопки:")
        for button in buttons:
            text = button.text.strip()
            if text and ("корзин" in text.lower() or "купить" in text.lower() or "добав" in text.lower()):
                print(f"  - '{text}'")
        
        # Ищем элементы с определенными классами
        cart_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='cart'], [class*='Cart'], [class*='basket'], [class*='Basket']")
        print(f"\nЭлементы с 'cart' в классе: {len(cart_elements)}")