class Config:
    BASE_URL = "https://mebelmart-saratov.ru"
    CATALOG_URL = f"{BASE_URL}/myagkaya_mebel_v_saratove/divanyi_v_saratove"
    
    # Настройки браузеров
    BROWSERS = ["chrome", "firefox"]
    DEFAULT_BROWSER = "chrome"
    
    # Таймауты
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 30
    PAGE_LOAD_TIMEOUT = 30
    
    # Тестовые данные
    TEST_PRODUCT_NAME = "Чебурашка"  # Название дивана, который точно есть
    TEST_PRODUCT_FULL_NAME = "Диван Чебурашка"
    TEST_PRICE_MIN = 10000
    TEST_PRICE_MAX = 15000
    
    # Пути
    SCREENSHOTS_DIR = "screenshots"
    ALLURE_RESULTS_DIR = "allure-results"