import pytest
from utils.driver_factory import DriverFactory
from utils.allure_helper import AllureHelper
from config.config import Config
from loguru import logger

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=Config.DEFAULT_BROWSER)
    parser.addoption("--headless", action="store_true", default=Config.HEADLESS)

@pytest.fixture(scope="function")
def driver(request):
    """Фикстура для создания и закрытия драйвера"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    logger.info(f"Запуск теста в {browser}, headless={headless}")
    driver = DriverFactory.create_driver(browser, headless)
    
    yield driver
    
    if request.node.rep_call.failed:
        logger.error(f"Тест {request.node.name} упал")
        AllureHelper.attach_screenshot(driver)
    
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)