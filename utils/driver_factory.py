from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config
from loguru import logger

class DriverFactory:
    """Фабрика для создания драйверов браузеров"""
    
    @staticmethod
    def create_driver(browser_name: str = Config.DEFAULT_BROWSER, headless: bool = Config.HEADLESS):
        """Создает и возвращает драйвер для указанного браузера"""
        logger.info(f"Запуск браузера: {browser_name}, headless={headless}")
        
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            
        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}")
        
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        return driver