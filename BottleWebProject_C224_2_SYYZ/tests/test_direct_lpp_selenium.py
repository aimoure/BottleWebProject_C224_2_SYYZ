import unittest
import threading
import time
import socket
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import app

logging.basicConfig(level=logging.INFO) # Настройка глобального уровеня логирования на INFO, чтобы отображать сообщения информационного уровня и выше
logger = logging.getLogger(__name__) # Создание логгера, привязанного к текущему модулю, для удобной отладки и вывода сообщений

class TestDirectLPPPractice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Поиск свободного порта и сборка базового URL
        cls.port = cls._get_free_port()  # Поиск свободного TCP-порт на локальной машине и его сохранение в атрибут класса
        cls.base_url = f"http://localhost:{cls.port}" # Формирование базового URL для запросов к серверу с учётом найденного порта

        # Запуск Bottle-сервера в фоне
        # Создание daemon-потока, который запускает HTTP-сервер Bottle на указанном порту
        cls.server_thread = threading.Thread(
            target=cls._run_server, args=(cls.port,), daemon=True
        )
        cls.server_thread.start() # Запуск потока, чтобы сервер начал принимать подключения

        # Пауза, пока сервер поднимется
        time.sleep(2)

    @classmethod
    # (после всех тестов)
    def tearDownClass(cls):
        # Daemon-поток сервера завершится вместе с тестами
        pass

    @classmethod
    # Вспомогательный метод для получения свободного порта
    def _get_free_port(cls):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создание нового TCP-сокет
        sock.bind(('', 0)) # Привязка сокета к любому интерфейсу и свободному порту
        port = sock.getsockname()[1] # Получение номера реально выделенного порта
        sock.close() # Закрытие сокета, освобождая порт
        logger.info(f"Found free port: {port}") # Логирование информации о найденном порте
        return port # Возврат номера найденного порта

    @classmethod
    def _run_server(cls, port):
        from bottle import run, default_app
        run(app=default_app(), host='localhost', port=port, quiet=True)

    # (перед каждым тестом)
    def setUp(self):
        # Selenium Manager настраивает двайвера для запуска для работы с браузером
        options = Options() # Создание объекта настроек для Chrome
        self.driver = webdriver.Chrome(options=options) # Инициализация Selenium WebDriver, используя встроенный Selenium Manager для подбора драйвера
        self.driver.implicitly_wait(5) # Устанавка неявного ожидания в 5 секунд для поиска элементов

    # (после каждого теста)
    def tearDown(self):
        self.driver.quit() # Закрытие браузера и освобождение ресурсов WebDriver

    def run_lpp_test(self, objective, constraint_matrix, rhs):
        # Открытие страницы
        self.driver.get(f"{self.base_url}/direct_lpp_practice")

        num_vars = len(objective)
        num_constraints = len(constraint_matrix)

        # Установка переменных и ограничений
        self.driver.execute_script(
            f"document.getElementById('number_of_variables').value = '{num_vars}';"
            f"document.getElementById('number_of_constraints').value = '{num_constraints}';"
            "window.redraw();"
        )
        time.sleep(1)

        # Ввод целевой функции
        for i, val in enumerate(objective):
            field = self.driver.find_element(By.NAME, f'x_{i}')
            field.clear()
            field.send_keys(str(val))

        # Ввод ограничений
        for i, row in enumerate(constraint_matrix):
            for j, val in enumerate(row):
                self.driver.find_element(By.NAME, f'cons_{i}_{j}').send_keys(str(val))
            self.driver.find_element(By.NAME, f'cons_rhs_{i}').send_keys(str(rhs[i]))

        # Решить
        solve_btn = self.driver.find_element(
            By.CSS_SELECTOR, "button[name='action'][value='solve']"
        )
        solve_btn.click()
        # Прокрутка вниз, чтобы область с результатом точно была видна
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Пауза для отрисовки результатов
        time.sleep(6)

        # Ожидание появления результата
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "results"))
        )
        result_text = self.driver.find_element(By.ID, 'results').text

        # Проверка результата
        accepted_phrases = [
            "Оптимальные", "Нет допустимого решения", "Ошибка",
            "Невозможно", "Решение не найдено"
        ]
        self.assertTrue(
            any(phrase in result_text for phrase in accepted_phrases),
            msg="Ожидалось сообщение об оптимуме или ошибке, но результат: " + result_text
        )

    def test_various_lpp_inputs(self):
        # Стандартная задача с допустимым решением
        # Maximize Z = 5x + 4y + 3z + 6w
        # При ограничениях, допускающих область допустимых решений
        self.run_lpp_test(
            objective=['3', '5', '2', '4'],
            constraint_matrix=[
                ['1', '2', '1', '0'],   # x + y + z ≤ 40
                ['2', '1', '0', '1'],   # 2x + 3y + 1w ≤ 50
                ['1', '1', '1', '1'],   # x + y + z + w ≤ 60
                ['0', '1', '2', '2'],   # y + 2z + 2w ≤ 50
                ['1', '0', '1', '0']    # x + z ≤ 30
            ],
            rhs=['40', '50', '60', '50', '30']
        )

        # Задача без допустимого решения
        # Все переменные ограничены сверху 1, но сумма ≤ 0 — несовместимо
        self.run_lpp_test(
            objective=['1', '1', '1', '1'],
            constraint_matrix=[
                ['1', '1', '0', '0'],   # x + y ≤ 2
                ['-1', '-1', '0', '0'],   # -x - y ≤ -5
                ['0', '0', '1', '0'],   # z ≤ 10
                ['0', '0', '0', '1'],   # w ≤ 10
                ['1', '0', '1', '0']    # x + z ≤ 100 (противоречие)
            ],
            rhs=['2', '-5', '10', '10', '100']
        )

        # Допустимая задача с перекрёстными ограничениями
        # Maximize Z = 4x + 2y + 5z + 3w
        # Зависимости между переменными менее прямолинейные, но допустимы
        self.run_lpp_test(
            objective=['4', '2', '5', '3'],
            constraint_matrix=[
                ['1', '2', '0', '1'],   # x + 2y + w ≤ 35
                ['0', '0', '2', '3'],   # 2z + 3w ≤ 40
                ['2', '0', '1', '1'],   # 2x + z + w ≤ 45
                ['1', '1', '1', '1'],   # x + y + z + w ≤ 50
                ['0', '3', '0', '1']    # 3y + w ≤ 30
            ],
            rhs=['35', '40', '45', '50', '30']
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)