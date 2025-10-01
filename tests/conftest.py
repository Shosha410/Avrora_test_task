import logging
import os
import time

import pytest

from pages import *
from utils import generate_random_string
from utils.driver_factory import create_driver

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def setup_logging(project_root):
    """Настройка логирования для проекта."""
    logs_dir = os.path.join(project_root, "send_results", "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"Создана директория логов: {logs_dir}")
    else:
        print(f"Директория логов уже существует: {logs_dir}")

    log_file = os.path.join(logs_dir, "test.log")
    logging.basicConfig(level=logging.INFO,
                        filename=log_file,
                        filemode="w",
                        format='%(asctime)s - %(levelname)s - %(message)s')
    loggers = logging.getLogger(__name__)
    loggers.info("Логирование настроено")
    return loggers


logger = setup_logging(PROJECT_ROOT)


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests on"
    )


@pytest.fixture(scope="session")
def driver(request):
    browser = request.config.getoption("--browser")

    driver = create_driver(browser)

    logger.info(f"Запущен браузер {browser}")
    logger.info(f"Версия браузера: {driver.capabilities.get('browserVersion')}")
    logger.info(f"Версия драйвера: {driver.capabilities.get('chrome', {}).get('chromedriverVersion')}")

    yield driver
    logger.info("Браузер закрыт")
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    test_name = item.name
    logger.info(f"Начало теста: {test_name}")
    item.start_time = time.time()
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    test_name = item.name
    yield
    end_time = time.time()
    duration = end_time - item.start_time
    logger.info(f"Конец теста: {test_name}.  Время выполнения: {duration:.2f} секунд")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    test_name = item.name
    if rep.when == "call":
        if rep.passed:
            logger.info(f"Тест '{test_name}' успешно пройден")
        elif rep.failed:
            logger.error(f"Тест '{test_name}' провален: {rep.longreprtext}")
        elif rep.skipped:
            logger.warning(f"Тест '{test_name}' пропущен: {rep.longreprtext}")

    return rep


@pytest.fixture(scope="session")
def random_test_data():
    """
    Генерация случайных данных для тестов
    """
    test_password = generate_random_string(10)
    test_name = generate_random_string(6)
    test_surname = generate_random_string(6)
    username = generate_random_string(6)

    return {"password": test_password,
            "name": "Test " + test_name,
            "surname": "Test " + test_surname,
            "username": username
            }


@pytest.fixture(scope="session")
def stash():
    """Session-scoped stash fixture."""
    return {}


@pytest.fixture(scope="function")
def welcome_page(driver):
    """Фикстура для создания экземпляра WelcomePage."""
    return WelcomePage(driver)


@pytest.fixture(scope="function")
def registration_page(driver):
    """Фикстура для создания экземпляра RegistrationPage."""
    return RegistrationPage(driver)


@pytest.fixture(scope="function")
def main_page(driver):
    """Фикстура для создания экземпляра MainPage."""
    return MainPage(driver)
