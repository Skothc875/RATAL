#!/usr/bin/python3
#####################################TELEGASERVER################################################ by Skothc875
# Version: Beta 0.1


import config
import os
import telebot
import hashlib
import subprocess
import codecs
aut = False
hashpass = config.hashpass
command = []
path = ''
try:
    bot = telebot.TeleBot(config.token)
except:
    print("Не удалосьзапустить бота:(")
rep_send = ''

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - твой компьютер.\n/auth - аунтификация на сервере\n/system - осуществляет доступ к серверу.\nБолее подробно о командах бота в документации.".format(message.from_user, bot.get_me()), parse_mode='html')
    

@bot.message_handler(commands=['auth'])
def auth1(message):
    global rep_send
    rep_send = bot.send_message(message.chat.id, "Введите пароль от сервера для аунтефикации.")

    bot.register_next_step_handler(rep_send, auth2)


def auth2(message):
    global aut
    if hashlib.sha256(message.text.encode('utf-8')).hexdigest() == hashpass:

        bot.delete_message(message.chat.id, message.message_id)
        aut = True
        bot.send_message(message.chat.id, "Аутентификация прошла успешо.")
        return
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Пароль не верный")


@bot.message_handler(commands=['system'])
def system(message):
    global aut
    if message.chat.type == 'private':
        if aut == True:
            bot.register_next_step_handler(bot.send_message(message.chat.id, "Введите команду."), start_cm)
        else:
            bot.send_message(message.chat.id, "У вас нет доступа.")


def start_cm(message):
    global command
    global path
    command = message.text.split()
    command1 = command.pop(0)

    if command1 == 'cd':
        path = command.pop(0)
        changing_directory(path, message)

    elif command1 == '/download':
        bot.register_next_step_handler(
        bot.send_message(message.chat.id, "Выберите файл который хотите загрузить из данной дерриктории."),
        download)

    elif command1 == '/upload':
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, "Выберите файл который хотите выгрузить в данную деррикторию."),
            upload)

    elif command1 == '/out':
        disconnect(message)


    elif subprocess.call(message.text, shell=True) == 0:

        try:
            bot.send_message(message.chat.id, subprocess.check_output(message.text, shell=True))
        except:
            subprocess.call(message.text, shell=True)
        bot.register_next_step_handler(bot.send_message(message.chat.id, subprocess.check_output("pwd", shell=True) + subprocess.check_output("whoami", shell=True)), start_cm)

    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Произошла ошибка при выполнении команды. Код ошибки: " + str(subprocess.call(message.text, shell=True))), start_cm)


def changing_directory(path, message):
    os.chdir(path)
    bot.register_next_step_handler(bot.send_message(message.chat.id, subprocess.check_output("pwd", shell=True) + subprocess.check_output("whoami", shell=True)), start_cm)


def download(message):
    if message.text == '/cancel':
        system(message)
    file = open(message.text, "rb")
    try:
        bot.send_document(message.chat.id, file)
    
    except:
        bot.register_next_step_handler(bot.send_message(message.chat.id, "Ошибка при отправке файла,проверьре назваие файла."), start_cm)

def upload(message):
    try:
        chat_id = message.chat.id
        now_dir = codecs.decode(subprocess.check_output("pwd", shell=True), 'UTF-8')
        now_dir = now_dir[:-1]

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = now_dir + "/" + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Файл успешно сохранён в дерриктории " + now_dir)
    except Exception as e:
        bot.reply_to(message, e)

def disconnect(message):
    global aut
    aut = False
    bot.send_message(message.chat.id, "Отключение от сервера...")
    
try:
    bot.polling(none_stop=True)


except:
    print("Ошибка при иницилизации бота.(Не стабильный интернет)")




