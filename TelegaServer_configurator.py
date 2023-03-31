import hashlib
import subprocess
try:
    import telebot
except:
    subprocess.call("pip install telebot", shell=True)
token = input("Введите токен который будет использоваться в боте: ")
passwd = input("Введите пароль который будет использоваться в боте: ")
conffile = open('config.py', 'w', encoding='utf-8')
conffile.write("hashpass = '" + hashlib.sha256(passwd.encode('utf-8')).hexdigest() + "'\n")
conffile.write("token = '" + token + "'\n")
print("Файл успешно сконфигурирован")
        

