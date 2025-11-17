# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

from pathlib import Path
from config import PATH_HTML
# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """
        Метод для обработки входящих GET-запросов
        """
        if self.path.startswith('/css'):
            file_path = self.path[1:]  # Убираем ведущий слэш
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                with open(file_path, 'r') as file:

                    self.wfile.write(bytes(file.read(), "utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        else:
            self.send_response(200)  # Отправка кода ответа
            self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
            self.end_headers()  # Завершение формирования заголовков ответа
            with open(PATH_HTML, 'r', encoding='utf-8') as file:
                html_content = file.read()
            self.wfile.write(bytes(html_content, "utf-8"))  # Тело ответа



    def do_POST(self):
        """Метод для обработки входящих POST-запросов"""
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    """ Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше"""
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Старт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
