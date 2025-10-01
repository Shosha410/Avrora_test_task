import time

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    """
    Page Object для страницы регистрации.
    """

    FIRSTNAME_INPUT_LOCATOR = (By.CSS_SELECTOR, "#firstname")
    LASTNAME_INPUT_LOCATOR = (By.CSS_SELECTOR, "#lastname")
    USERNAME_INPUT_LOCATOR = (By.CSS_SELECTOR, "#userName")
    PASSWORD_INPUT_LOCATOR = (By.CSS_SELECTOR, "#password")
    CAPTCHA_BUTTON_LOCATOR = (By.CSS_SELECTOR, ".recaptcha-checkbox-border")
    CAPTCHA_IFRAME_LOCATOR = (By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
    SUBMIT_BUTTON_LOCATOR = (By.CSS_SELECTOR, "#register")
    REGISTRATION_SUCCESS_TEXT_LOCATOR = (By.CSS_SELECTOR, "p.sent-text")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Ввод данных в форму регистрации")
    def enter_registration_data(self, firstname, lastname, username, password):
        """
        Ввод данных в форму регистрации
        """
        firstname_input = self.wait_for_element_to_be_clickable(self.FIRSTNAME_INPUT_LOCATOR)
        lastname_input = self.wait_for_element_to_be_clickable(self.LASTNAME_INPUT_LOCATOR)
        username_input = self.wait_for_element_to_be_clickable(self.USERNAME_INPUT_LOCATOR)
        password_input = self.wait_for_element_to_be_clickable(self.PASSWORD_INPUT_LOCATOR)

        with self.handle_element_action("Can't enter registration data"):
            firstname_input.send_keys(firstname)
            lastname_input.send_keys(lastname)
            username_input.send_keys(username)
            password_input.send_keys(password)

    @allure.step("Нажатие на капчу")
    def click_captcha_button(self):
        """
        Нажатие на кнопку капчу с переключением в iframe
        """
        with self.handle_element_action("Can't click on the captcha button"):
            iframe = self.wait_for_element_to_be_present(self.CAPTCHA_IFRAME_LOCATOR)
            self.driver.switch_to.frame(iframe)
            captcha_checkbox = self.wait_for_element_to_be_clickable(self.CAPTCHA_BUTTON_LOCATOR)
            captcha_checkbox.click()
            self.driver.switch_to.default_content()

    @allure.step("Нажатие на кнопку 'Зарегистрироваться'")
    def click_submit_button(self):
        """
        Нажатие на кнопку "Зарегистрироваться"
        """
        with self.handle_element_action("Can't click on the registration button"):
            submit_button = self.wait_for_element_to_be_clickable(self.SUBMIT_BUTTON_LOCATOR)
            submit_button.click()

    @allure.step("Принятие alert")
    def accept_alert(self, timeout=60):
        """
        Принятие всплывающего alert.
        """
        wait = WebDriverWait(self.driver, timeout)
        try:
            alert = wait.until(ec.alert_is_present())
            alert.accept()
            return True
        except TimeoutError:
            time.sleep(2)
            self.attach_screenshot("Success authorization")
            return False
