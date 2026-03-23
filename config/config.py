class Config:
    """Конфигурация для UI тестов"""
    
    # Базовый URL
    BASE_URL = "https://mebelmart-saratov.ru"
    CATALOG_URL = f"{BASE_URL}/myagkaya_mebel_v_saratove/divanyi_v_saratove"
    
    # Настройки браузера
    DEFAULT_BROWSER = "chrome"  # chrome или firefox
    HEADLESS = False  # headless режим
    
    # Таймауты
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
    
    # Тестовые данные
    TEST_SOFA_NAME = "Диван ЧБ"
    TEST_SOFA_PRICE = 12015