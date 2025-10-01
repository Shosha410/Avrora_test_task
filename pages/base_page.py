from contextlib import contextmanager

import allure
import pytest
from allure_commons.types import AttachmentType
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """
    Базовый класс для Page Object
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_for_element_to_be_clickable(self, locator, timeout=60):
        """
        Ожидание, пока элемент станет кликабельным
        """
        return WebDriverWait(self.driver, timeout).until(
            ec.element_to_be_clickable(locator)
        )

    def wait_for_element_to_be_present(self, locator, timeout=60):
        """
        Ожидание, пока элемент появится в DOM
        """
        return WebDriverWait(self.driver, timeout).until(
            ec.presence_of_element_located(locator)
        )

    def wait_for_element_to_be_visible(self, locator, timeout=60):
        """
        Ожидание, пока элемент станет видимым на странице
        """
        return WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(locator)
        )

    def attach_screenshot(self, name):
        """Прикрепляет скриншот к отчету Allure"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=AttachmentType.PNG,
        )

    @contextmanager
    def handle_element_action(self, description):
        """
        Контекстный менеджер для обработки действий с элементами с обработкой ошибок и скриншотами
        """
        try:
            yield
        except Exception as e:
            self.attach_screenshot(description)
            pytest.fail(f"{description}")
            raise e

    @contextmanager
    def handle_element_check(self, description):
        """
        Контекстный менеджер для обработки проверок assert с обработкой ошибок и скриншотами
        """
        try:
            yield
        except AssertionError as e:
            self.attach_screenshot(description)
            pytest.fail(f"{description}")
            raise AssertionError(f"{description}: {e}")
