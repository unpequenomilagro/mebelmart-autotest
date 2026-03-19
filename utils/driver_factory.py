from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config
from loguru import logger
import tempfile
import os
import uuid

class DriverFactory:
    """Фабрика для создания драйверов браузеров"""
    
    @staticmethod
    def create_driver(browser_name: str = Config.DEFAULT_BROWSER, headless: bool = False):
        """
        Создает и возвращает драйвер для указанного браузера
        """
        logger.info(f"Запуск браузера: {browser_name}, headless={headless}")
        
        # Уникальный идентификатор для изоляции профилей
        unique_id = str(uuid.uuid4())[:8]
        
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            
            # Основные настройки
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--incognito")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option("detach", True)
            
            # Headless режим для параллельного запуска
            if headless:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
            
            # Уникальная директория для пользовательских данных
            user_data_dir = os.path.join(tempfile.gettempdir(), f"chrome_test_profile_{unique_id}")
            options.add_argument(f"--user-data-dir={user_data_dir}")
            
            # Таймауты
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
            
        elif browser_name.lower() == "firefox":
            # Создаем временный профиль с уникальным именем
            temp_profile_dir = os.path.join(tempfile.gettempdir(), f"firefox_test_profile_{unique_id}")
            os.makedirs(temp_profile_dir, exist_ok=True)
            
            options = FirefoxOptions()
            
            # Настройки окна
            if not headless:
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
            
            # Приватный режим
            options.add_argument("--private")
            
            # Headless режим для параллельного запуска
            if headless:
                options.add_argument("--headless")
            
            # Отключаем уведомления
            options.set_preference("dom.webnotifications.enabled", False)
            options.set_preference("dom.push.enabled", False)
            
            # Настройки для стабильности
            options.set_preference("browser.startup.homepage", "about:blank")
            options.set_preference("browser.startup.page", 0)
            options.set_preference("browser.cache.disk.enable", False)
            options.set_preference("browser.cache.memory.enable", False)
            options.set_preference("browser.cache.offline.enable", False)
            options.set_preference("network.http.use-cache", False)
            options.set_preference("browser.sessionstore.resume_from_crash", False)
            options.set_preference("browser.sessionstore.max_tabs_undo", 0)
            options.set_preference("browser.tabs.remote.autostart", False)
            
            # Важно для параллельного запуска - отключаем блокировки профиля
            options.set_preference("browser.tabs.remote.autostart.2", False)
            options.set_preference("browser.sessionstore.restore_on_demand", False)
            options.set_preference("browser.sessionstore.restore_tabs_lazily", False)
            
            # Указываем путь к временному профилю
            profile = FirefoxProfile(temp_profile_dir)
            profile.set_preference("browser.startup.homepage", "about:blank")
            profile.set_preference("browser.startup.page", 0)
            options.profile = profile
            
            # Явно указываем путь к Firefox
            firefox_paths = [
                "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe",
            ]
            
            for path in firefox_paths:
                if os.path.exists(path):
                    options.binary_location = path
                    logger.info(f"Найден Firefox по пути: {path}")
                    break
            
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}")
        
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        
        if not headless and browser_name.lower() == "chrome":
            driver.maximize_window()
        
        logger.info(f"Браузер {browser_name} успешно запущен с ID {unique_id}")
        return driver