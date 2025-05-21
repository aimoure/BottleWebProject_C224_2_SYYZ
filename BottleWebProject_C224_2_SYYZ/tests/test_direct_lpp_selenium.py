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

    def test_filling_out_and_solving(self):
        # Открытие нужной страницы
        self.driver.get(f"{self.base_url}/direct_lpp_practice")

        # Проверка, что по умолчанию number_of_variables == 2
        num_vars = self.driver.find_element(By.ID, 'number_of_variables')
        self.assertEqual(num_vars.get_attribute('value'), '2')

        # Ввод в целевую функцию 3 и 2
        self.driver.find_element(By.NAME, 'x_0').clear()
        self.driver.find_element(By.NAME, 'x_0').send_keys('3')
        self.driver.find_element(By.NAME, 'x_1').clear()
        self.driver.find_element(By.NAME, 'x_1').send_keys('2')

        # Увеличение number_of_constraints до 2 и перерисовка таблицы
        self.driver.execute_script(
            "document.getElementById('number_of_constraints').value = '2';"
            "window.redraw();"
        )
        time.sleep(0.5)  # Пауза для JS завершить отрисовку

        # Заполнение матрицы ограничений
        self.driver.find_element(By.NAME, 'cons_0_0').send_keys('2')
        self.driver.find_element(By.NAME, 'cons_0_1').send_keys('1')
        self.driver.find_element(By.NAME, 'cons_1_0').send_keys('1')
        self.driver.find_element(By.NAME, 'cons_1_1').send_keys('2')

        # Заполнение свободных членов
        self.driver.find_element(By.NAME, 'cons_rhs_0').send_keys('4')
        self.driver.find_element(By.NAME, 'cons_rhs_1').send_keys('4')

        # Нажатие кнопки Решить
        btn = self.driver.find_element(
            By.CSS_SELECTOR, "button[name='action'][value='solve']"
        )
        btn.click()

        # Пауза, пока в блоке #results появится заголовок <h3>
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#results h3"))
        )

        # Проверка, что результат явно содержит слово "Оптимальные"
        text = self.driver.find_element(By.ID, 'results').text
        self.assertIn("Оптимальные", text)

if __name__ == '__main__':
    unittest.main(verbosity=2)