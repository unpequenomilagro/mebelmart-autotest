import allure
from datetime import datetime
from pathlib import Path
from config.config import Config

class AllureHelper:
    """Хелпер для работы с Allure"""
    
    @staticmethod
    def attach_screenshot(driver, name="Скриншот"):
        """Прикрепляет скриншот к отчету Allure"""
        try:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")
    
    @staticmethod
    def attach_page_source(driver, name="HTML страницы"):
        """Прикрепляет HTML страницы к отчету"""
        try:
            allure.attach(
                driver.page_source,
                name=name,
                attachment_type=allure.attachment_type.HTML
            )
        except Exception as e:
            print(f"Не удалось получить HTML: {e}")
    
    @staticmethod
    def attach_logs(driver, name="Логи браузера"):
        """Прикрепляет логи браузера к отчету"""
        try:
            logs = driver.get_log("browser")
            if logs:
                allure.attach(
                    "\n".join([str(log) for log in logs]),
                    name=name,
                    attachment_type=allure.attachment_type.TEXT
                )
        except:
            pass  # Не все драйверы поддерживают получение логов