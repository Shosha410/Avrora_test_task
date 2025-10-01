import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
#from webdriver_manager.chrome import ChromeDriverManager
#import undetected_chromedriver as uc
from config.test_data import USER_AGENTS


def create_driver(browser):
    """
    Создание и возврат драйвера браузера на основе переданных аргументов
    """

    if browser.lower() == "chrome":
        chrome_options = ChromeOptions()
        #chrome_options = uc.ChromeOptions()
        #chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("prefs", {
            "safebrowsing.enabled": True,
            "excludeSwitches": ["enable-automation"],
            'useAutomationExtension': False
        })

        #service = Service(executable_path=ChromeDriverManager().install())
        #driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver = uc.Chrome(options=chrome_options)

        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
        chrome_binary_path = os.environ.get("CHROME_BIN", "/usr/bin/chromium")

        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError(f"ChromeDriver not found at: {chromedriver_path}")
        if not os.path.exists(chrome_binary_path):
            raise FileNotFoundError(f"Chrome binary not found at: {chrome_binary_path}")

        chrome_options.binary_location = chrome_binary_path

        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    return driver
