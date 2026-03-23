import allure
import time
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from config.config import Config
from loguru import logger

@allure.feature("Корзина")
class TestCart:
    
    @allure.title("Добавление дивана в корзину")
    def test_add_to_cart(self, driver):
        catalog = CatalogPage(driver)
        catalog.open_catalog()
        
        # Даем время на полную загрузку
        time.sleep(2)
        
        index, product = catalog.find_sofa_by_name("Диван ЧБ")
        assert index != -1, "Диван не найден"
        
        catalog_name = catalog.get_product_title_by_index(index)
        logger.info(f"Найден товар: {catalog_name}")
        
        catalog.click_on_product(index)
        logger.info("Переход на страницу товара")
        time.sleep(2)
        
        product_page = ProductPage(driver)
        product_page.verify_product_page("Чебурашка")
        
        product_page.add_to_cart()
        
        cart = CartPage(driver)
        cart.open(Config.BASE_URL + "/cart")
        time.sleep(2)
        
        assert cart.is_product_in_cart("Чебурашка"), "Товар не в корзине"
        logger.info("Тест пройден: товар в корзине")