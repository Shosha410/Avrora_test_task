import allure
from allure_commons.types import Severity
from selenium.webdriver.remote.webdriver import WebDriver

from pages import WelcomePage, RegistrationPage, MainPage
from utils.helper import load_test_data_from_package

TEST_DATA = load_test_data_from_package("config", "test_data.json")


class TestAuthorization:

    @allure.title("Авторизация с валидными данными")
    @allure.feature("Авторизация")
    @allure.severity(Severity.BLOCKER)
    def test_authorization(self, driver: WebDriver, welcome_page: WelcomePage, registration_page: RegistrationPage,
                           main_page: MainPage, stash):
        driver.get(TEST_DATA["login_url"])
        username = stash.get('username')
        password = stash.get('password')
        welcome_page.enter_authorization_data(username, password)
        main_page.check_authorization_success_text()
