import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    """
    Page Object для главной страницы
    """

    LOGOUT_TEXT_LOCATOR = (By.CSS_SELECTOR, "#submit")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Проверка наличия текста после авторизации")
    def check_authorization_success_text(self, expected_text="Log out"):
        """
        Проверка наличия текста после авторизации
        """
        with self.handle_element_check("Something went wrong after user registration"):
            success_text_element = self.wait_for_element_to_be_present(self.LOGOUT_TEXT_LOCATOR)
            assert success_text_element.text == expected_text, f"Expected text '{expected_text}', but got " \
                                                               f"'{success_text_element}'"
