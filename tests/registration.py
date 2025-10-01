import allure
from allure_commons.types import Severity
from selenium.webdriver.remote.webdriver import WebDriver

from pages import WelcomePage, RegistrationPage
from utils.helper import load_test_data_from_package

TEST_DATA = load_test_data_from_package("config", "test_data.json")


class TestRegistration:

    @allure.title("Регистрация с валидными данными")
    @allure.feature("Регистрация")
    @allure.severity(Severity.BLOCKER)
    def test_registration(self, driver: WebDriver, welcome_page: WelcomePage, registration_page: RegistrationPage,
                          random_test_data, stash):
        driver.get(TEST_DATA["login_url"])
        welcome_page.check_title()
        welcome_page.click_registration_link()
        registration_page.click_captcha_button()
        firstname = random_test_data['name']
        lastname = random_test_data['surname']
        username = random_test_data['username']
        password = random_test_data['password']
        stash['username'] = username
        stash['password'] = password
        registration_page.enter_registration_data(firstname, lastname, username, password)
        registration_page.click_submit_button()
        registration_page.accept_alert()
