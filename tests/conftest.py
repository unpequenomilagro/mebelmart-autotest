import pytest
from utils.driver_factory import DriverFactory
from utils.allure_helper import AllureHelper
from config.config import Config
from loguru import logger
import allure
import os
import tempfile
import shutil

def pytest_addoption(parser):
    """Добавляем опции командной строки"""
    parser.addoption(
        "--browser",
        action="store",
        default=Config.DEFAULT_BROWSER,
        help="Выбор браузера: chrome, firefox или all"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск в headless режиме"
    )

@pytest.fixture(scope="function")
def driver(request):
    """Фикстура для создания и закрытия драйвера"""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    # Если указан параметр all, то используем параметризацию
    if hasattr(request, 'param'):
        browser_name = request.param
    
    logger.info(f"Запуск теста в браузере: {browser_name}, headless={headless}")
    
    # Очищаем старые временные профили перед запуском
    cleanup_temp_profiles()
    
    driver = None
    try:
        # Создаем драйвер
        driver = DriverFactory.create_driver(browser_name, headless)
        
        # Передаем драйвер в тест
        yield driver
        
    except Exception as e:
        logger.error(f"Ошибка при создании драйвера: {e}")
        raise
    
    finally:
        # После теста делаем скриншот если тест упал
        if driver and hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            logger.error(f"Тест {request.node.name} упал. Делаем скриншот...")
            AllureHelper.attach_screenshot(driver, f"Ошибка_в_тесте_{request.node.name}")
            AllureHelper.attach_page_source(driver)
        
        # Закрываем браузер
        if driver:
            logger.info("Закрытие браузера")
            driver.quit()

def pytest_generate_tests(metafunc):
    """Параметризация тестов для запуска на разных браузерах"""
    if "driver" in metafunc.fixturenames:
        browser = metafunc.config.getoption("--browser")
        if browser == "all":
            # Запускаем тесты на всех браузерах
            metafunc.parametrize("driver", ["chrome", "firefox"], indirect=True)
        else:
            # Запускаем только на указанном браузере
            metafunc.parametrize("driver", [browser], indirect=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для получения результата теста"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def cleanup_temp_profiles():
    """Очистка временных профилей браузеров"""
    try:
        temp_dir = tempfile.gettempdir()
        for item in os.listdir(temp_dir):
            if item.startswith(("chrome_test_profile_", "firefox_test_profile_")):
                try:
                    shutil.rmtree(os.path.join(temp_dir, item))
                    logger.debug(f"Удален временный профиль: {item}")
                except:
                    pass
    except Exception as e:
        logger.debug(f"Ошибка при очистке временных профилей: {e}")