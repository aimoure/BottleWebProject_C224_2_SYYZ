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

# Импортируем сервер из твоего app.py
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
        time.sleep(2)  # Ждём запуска сервера

    def setUp(self):
        chrome_options = Options()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

    def test_navigation_to_purpose_theory(self):
        # Открываем главную страницу
        self.driver.get(f'http://localhost:{self.port}/')

        # Убедимся, что заголовок страницы правильный
        h1_text = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(h1_text, 'DualSolve')

        # Находим и нажимаем на ссылку "Задача о назначениях"
        purpose_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/purpose_theory']"))
        )
        purpose_link.click()

        # Ждём загрузки страницы и появления заголовка
        header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )


        # Задержка 3 секунды
        time.sleep(3)

        # Прокрутка вниз
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Клик по кнопке "Перейти к решению"
        practice_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/purpose_practice']"))
        )
        practice_button.click()

        # Задержка 3 секунды после перехода на страницу калькулятора
        time.sleep(3)

            # Устанавливаем размер матрицы = 3
        matrix_size_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'size'))
        )
        matrix_size_input.clear()
        matrix_size_input.send_keys('3')
        time.sleep(1)

        

        # Заполняем матрицу случайными числами от 0 до 10
        for i in range(3):
            for j in range(3):
                cell = self.driver.find_element(By.NAME, f'matrix-{i}-{j}')
                cell.clear()
                cell.send_keys(str(random.randint(0, 10)))

        # Нажимаем кнопку "Решить задачу"
        solve_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'result'))
        )
        solve_button.click()

        # Прокрутка вниз
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Обновление страницы
        self.driver.refresh()
        time.sleep(1)  # Дай странице загрузиться

        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1) 
        # Установить чекбокс "решить задачу на максимум"
        maximize_checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'maximize'))
        )
        if not maximize_checkbox.is_selected():
            maximize_checkbox.click()

        # Нажать кнопку "Сгенерировать рандомно"
        generate_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'uploadRandomBtn'))
        )
        generate_button.click()

        # Прокрутка вниз снова
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        # Нажимаем кнопку "Решить задачу"
        solve_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'result'))
        )
        solve_button.click()
        time.sleep(3)



if __name__ == '__main__':
    unittest.main()
