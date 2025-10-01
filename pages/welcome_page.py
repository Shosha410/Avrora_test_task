import time

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class WelcomePage(BasePage):
    """
    Page Object для страницы приветствия
    """

    USERNAME_INPUT_LOCATOR = (By.CSS_SELECTOR, "#userName")
    PASSWORD_INPUT_LOCATOR = (By.CSS_SELECTOR, "#password")
    REGISTRATION_LINK_LOCATOR = (By.CSS_SELECTOR, "#newUser")
    AUTHORIZATION_LINK_LOCATOR = (By.CSS_SELECTOR, "#login")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Проверка открытия страницы Welcome")
    def check_title(self, expected_title="DEMOQA"):
        """
        Проверка открытия страницы Welcome
        """
        with self.handle_element_check("Can't open Welcome Page"):
            actual_title = self.driver.title
            assert actual_title == expected_title, f"Expected title '{expected_title}', but got '{actual_title}'"

    @allure.step("Переход по нажатию кнопки 'Зарегистрироваться'")
    def click_registration_link(self):
        """
        Переход по нажатию кнопки "Зарегистрироваться"
        """
        with self.handle_element_action("Registration link click failed"):
            registration_link = self.wait_for_element_to_be_clickable(self.REGISTRATION_LINK_LOCATOR)
            registration_link.click()

    @allure.step("Ввод данных в форму регистрации")
    def enter_authorization_data(self, username=None, password=None):
        """
        Ввод данных в форму регистрации а также нажатие кнопки авторизации
        """
        username_input = self.wait_for_element_to_be_clickable(self.USERNAME_INPUT_LOCATOR)
        password_input = self.wait_for_element_to_be_clickable(self.PASSWORD_INPUT_LOCATOR)
        authorization_button = self.wait_for_element_to_be_clickable(self.AUTHORIZATION_LINK_LOCATOR)

        with self.handle_element_action("Can't enter registration data"):
            username_input.send_keys(username)
            password_input.send_keys(password)
            authorization_button.click()
            time.sleep(10)
            self.attach_screenshot("Success authorization")
