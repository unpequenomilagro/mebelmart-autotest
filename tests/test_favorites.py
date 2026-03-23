import allure
from pages.catalog_page import CatalogPage
from pages.favorites_page import FavoritesPage
from loguru import logger
import time

@allure.feature("Избранное")
class TestFavorites:
    
    @allure.title("Добавление товара в избранное")
    def test_add_to_favorites(self, driver):
        catalog = CatalogPage(driver)
        catalog.open_catalog()
        
        index, _ = catalog.find_sofa_by_name("Диван ЧБ")
        assert index != -1, "Диван не найден"
        
        catalog_name = catalog.get_product_title_by_index(index)
        logger.info(f"Найден товар: {catalog_name}")
        
        catalog.add_to_favorites(index)
        logger.info("Товар добавлен в избранное")
        time.sleep(1)
        
        catalog.go_to_favorites()
        logger.info("Переход в избранное")
        time.sleep(1)
        
        favorites = FavoritesPage(driver)
        # Проверяем по названию, которое отображается на странице избранного
        assert favorites.is_product_in_favorites("Чебурашка"), f"Товар 'Чебурашка' не в избранном"
        logger.info("Тест пройден: товар в избранном")