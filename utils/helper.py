import json
import os
import random
import subprocess
from importlib.resources import files


def generate_random_string(length=10):
    """
    Генерация случайной строки, гарантированно содержащей все типы символов (альтернативный подход).
    """
    letters_s = "abcdefghijklmnopqrstuvwxyz"
    letters_l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    special_chars = "!@#$%^&*()_+=-`~[]}|;':,./<>?"

    characters = letters_s + letters_l + digits + special_chars

    result = [random.choice(characters) for _ in range(length - 4)]

    result.append(random.choice(letters_s))
    result.append(random.choice(letters_l))
    result.append(random.choice(digits))
    result.append(random.choice(special_chars))

    random.shuffle(result)
    return ''.join(result)


def generate_allure_report(allure_results_dir, allure_report_dir):
    """Генерирует Allure отчет."""
    subprocess.run(
        ["allure", "generate", allure_results_dir, "-o", allure_report_dir,
         "--clean", "--report-name", "Avrora Allure Report", "--single-file"],
        check=True, capture_output=True, text=True
    )
    return os.path.join(allure_report_dir, "index.html")


def load_test_data(filepath):
    """Загрузка тестовых данных из JSON файла."""
    with open(filepath, 'r') as f:
        return json.load(f)


def setup_allure_dirs(project_root, allure_results_dir_name="allure-results", allure_report_dir_name="allure-report"):
    """Создает allure directories, если они не существуют."""
    allure_results_dir = os.path.join(project_root, "send_results", allure_results_dir_name)
    allure_report_dir = os.path.join(project_root, "send_results", allure_report_dir_name)

    if not os.path.exists(allure_results_dir):
        os.makedirs(allure_report_dir)

    if not os.path.exists(allure_report_dir):
        os.makedirs(allure_report_dir)
    return allure_results_dir, allure_report_dir


def load_test_data_from_package(package, resource):
    """Загружает тестовые данные из файла внутри пакета."""
    package_path = files(package) / resource
    with open(package_path, 'r') as f:
        data = f.read()
    return json.loads(data)
