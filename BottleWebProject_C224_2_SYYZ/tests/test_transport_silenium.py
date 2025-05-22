
# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import socket
import logging
import random

# Импортируем сервер из app.py
import app

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    logger.info(f"Found free port: {port}")
    return port

def run_server(port):
    try:
        from bottle import run, default_app
        run(app=default_app(), host='localhost', port=port, quiet=True)
    except Exception as e:
        logger.error(f"Error starting server on port {port}: {e}")
        raise

class TestBottleApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = get_free_port()
        cls.server_thread = threading.Thread(target=run_server, args=(cls.port,))
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(3)  # Увеличено время ожидания запуска сервера

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")  # Для стабильности в некоторых окружениях
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)  # Увеличен таймаут до 15 секунд

    def tearDown(self):
        self.driver.quit()

    def test_full_navigation_and_interaction(self):
        try:
            # --- Часть 1: Главная страница (index.tpl) ---
            logger.info("Открываем главную страницу")
            self.driver.get(f'http://localhost:{self.port}/')

            # Проверяем заголовок страницы
            h1_text = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, 'h1'))
            ).text
            self.assertEqual(h1_text, 'DualSolve', "Заголовок главной страницы не соответствует ожидаемому")
            logger.info("Заголовок главной страницы проверен")

            # Прокрутка вниз
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Список ссылок на главной странице (на основе index.tpl)
            links = [
                "/transport_practice",
                "/purpose_practice",
                "/direct_lpp_practice",
                "/dual_lpp_practice"
            ]

            # Перебираем каждую кнопку, кликаем и возвращаемся назад
            for link_href in links:
                logger.info(f"Кликаем по ссылке: {link_href}")
                button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[@href='{link_href}' and contains(@class, 'btn')]"))
                )
                button.click()
                time.sleep(2)  # Ждём загрузки страницы
                self.driver.back()
                time.sleep(1)  # Ждём возврата на главную
                # Проверяем, что вернулись на главную
                h1_text = self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, 'h1'))
                ).text
                self.assertEqual(h1_text, 'DualSolve', f"Не удалось вернуться на главную страницу после клика на {link_href}")
                logger.info(f"Успешно вернулись на главную после {link_href}")

            # --- Часть 2: Страница транспортной задачи (transport_theory.tpl) ---
            logger.info("Переходим на страницу транспортной задачи через navbar")
            # Проверяем, если navbar свернут (для мобильных устройств)
            toggle_button = self.driver.find_elements(By.CLASS_NAME, 'navbar-toggle')
            if toggle_button and toggle_button[0].is_displayed():
                toggle_button[0].click()
                time.sleep(1)
                logger.info("Развернули navbar")

            transport_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//ul[@class='nav navbar-nav']//a[@href='/transport_theory']"))
            )
            transport_link.click()
            time.sleep(2)

            # Проверяем, что мы на странице транспортной задачи
            h1_text = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, 'h1'))
            ).text
            self.assertTrue('Транспортная задача' in h1_text, "Не удалось перейти на страницу транспортной задачи")
            logger.info("Успешно перешли на страницу транспортной задачи")

            # Прокрутка вниз до конца страницы
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Нажимаем на кнопку "Перейти к калькулятору" внизу (в секции calc-start-section)
            logger.info("Кликаем по кнопке 'Перейти к калькулятору' внизу")
            calc_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'calc-start-section')]//a[@href='/transport_practice' and contains(@class, 'btn')]"))
            )
            calc_button.click()
            time.sleep(2)

            # Возвращаемся назад
            self.driver.back()
            time.sleep(1)

            # Нажимаем на первую (верхнюю) кнопку "Перейти к калькулятору" (в jumbotron)
            logger.info("Кликаем по верхней кнопке 'Перейти к калькулятору'")
            first_calc_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'jumbotron')]//a[@href='/transport_practice' and contains(@class, 'btn')]"))
            )
            first_calc_button.click()
            time.sleep(2)

            # --- Часть 3: Страница калькулятора транспортной задачи (transport_practice.tpl) ---
            logger.info("Работаем на странице калькулятора транспортной задачи")

            # Нажимаем кнопку "Решить задачу"
            logger.info("Кликаем по кнопке 'Решить задачу'")
            solve_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and @value='solve' and contains(@class, 'btn-primary')]"))
            )
            solve_button.click()
            time.sleep(3)

            # Дважды нажимаем кнопку "Загрузить пример"
            logger.info("Дважды кликаем по кнопке 'Загрузить пример'")
            for _ in range(2):
                # Заново находим кнопку перед каждым кликом, чтобы избежать StaleElementReferenceException
                example_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'example-button') and contains(@class, 'btn-warning')]"))
                )
                example_button.click()
                time.sleep(2)  # Ждем завершения действия после клика
                logger.info("Успешно кликнули по кнопке 'Загрузить пример'")

            # Снова нажимаем "Решить задачу"
            logger.info("Снова кликаем по кнопке 'Решить задачу'")
            solve_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and @value='solve' and contains(@class, 'btn-primary')]"))
            )
            solve_button.click()
            time.sleep(3)

            # Нажимаем кнопку "Очистить"
            logger.info("Кликаем по кнопке 'Очистить'")
            clear_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and @value='clear' and contains(@class, 'btn-secondary')]"))
            )
            clear_button.click()
            time.sleep(2)

            # Снова нажимаем "Загрузить пример"
            logger.info("Снова кликаем по кнопке 'Загрузить пример'")
            example_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'example-button') and contains(@class, 'btn-warning')]"))
            )
            example_button.click()
            time.sleep(2)

            # Снова нажимаем "Решить задачу"
            logger.info("Финальный клик по кнопке 'Решить задачу'")
            solve_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and @value='solve' and contains(@class, 'btn-primary')]"))
            )
            solve_button.click()
            time.sleep(3)

            logger.info("Тест успешно завершен")

        except Exception as e:
            logger.error(f"Ошибка во время теста: {str(e)}")
            # Сохраняем скриншот для отладки
            self.driver.save_screenshot("error_screenshot.png")
            raise

if __name__ == '__main__':
    unittest.main()
