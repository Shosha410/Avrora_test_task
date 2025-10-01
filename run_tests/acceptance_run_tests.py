import os

import pytest

from utils.helper import generate_allure_report, setup_allure_dirs

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR = setup_allure_dirs(PROJECT_ROOT)

TEST_FILES = [
    os.path.join(PROJECT_ROOT, "tests", "registration.py"),
    os.path.join(PROJECT_ROOT, "tests", "authorization.py")
]

if __name__ == "__main__":
    pytest_args = ["-v",
                   f"--alluredir={ALLURE_RESULTS_DIR}",
                   *TEST_FILES]

    pytest.main(pytest_args)

    report_path = generate_allure_report(ALLURE_RESULTS_DIR, ALLURE_REPORT_DIR)
