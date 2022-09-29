"""Модуль бота, работающего через API vk.com с сообщениями группы.

функция write_msg отправляет сообщения пользователю.;
функция paste_foto отправляет фотографии пользователю.
"""
import configparser
import vk_api
import time
from random import randrange
from datetime import date
from psycopg2 import errors as err
import webbrowser
from selenium.common import exceptions
from sys import exit
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import get_code
from info_vk import VK_data
from VKinder_db_engine import DatabaseConfig


def write_msg(user_id: int, message: str, *keyboard):
    """Отправляет сообщения пользователю."""
    vk.messages.send(keyboard=keyboard, user_id=user_id, message=message, random_id=randrange(10 ** 9))


def paste_foto(user_id: int, attachment: str, *keyboard):
    """Отправляет фотографии пользователю."""
    vk.messages.send(keyboard=keyboard, user_id=user_id, attachment=attachment, random_id=randrange(10 ** 9))


if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()

        config.read("tokens.ini")
        # Токен от сообщества в VK
        vk_api_token = config['TOKEN_BOT']['token']
        # Личный токен пользователя для программы поиска
        if config['TOKEN_SEARCH']['token'] == '':
            try:
                token_program = get_code.get_token_vk()
            except exceptions.NoSuchWindowException:
                exit('Запустите программу заново и введите ключ авторизации корректно: либо в браузере, либо в файле tokens.ini')

        else:
            token_program = config['TOKEN_SEARCH']['token']

        config.read("base_settings.ini")
        # Название базы данных
        db_name = config["Database"]["db_name"]
        # Название пользователя базы данных
        user_name = config["Database"]["user_name"]
        # Пароль пользователя базы данных
        user_password = config["Database"]["user_password"]

        # Создание таблиц в базе данных
        vk_db = DatabaseConfig(db_name, user_name, user_password)
        vk_db.table_creation('vk_user', 'user_id_in_vk INTEGER PRIMARY KEY, '
                                        '          age INTEGER NOT NULL, '
                                        '       gender INTEGER NOT NULL, '
                                        '         city INTEGER NOT NULL')
        vk_db.table_creation('favorites', ' vk_user_id INTEGER PRIMARY KEY, '
                                          '       name VARCHAR(50), '
                                          '    surname VARCHAR(50), '
                                          'profile_url VARCHAR(100) UNIQUE NOT NULL, '
                                          '     photos VARCHAR(100)')
        vk_db.table_creation('user_favorites', '           id SERIAL PRIMARY KEY, '
                                               'user_id_in_vk INTEGER NOT NULL REFERENCES vk_user(user_id_in_vk), '
                                               '       fav_id INTEGER NOT NULL REFERENCES favorites(vk_user_id)')

        # Подключение бота к сообществу в VK
        vk_enter = vk_api.VkApi(token=vk_api_token)
        vk = vk_enter.get_api()
        longpoll = VkLongPoll(vk_enter)

        # Клавиатура 1
        keyboard1 = VkKeyboard(one_time=True)
        keyboard1.add_button('Поиск', color=VkKeyboardColor.PRIMARY)

        # Клавиатура 2
        keyboard2 = VkKeyboard(one_time=True)
        keyboard2.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
        keyboard2.add_button('Следующий', color=VkKeyboardColor.PRIMARY)
        keyboard2.add_line()
        keyboard2.add_button('В избранное', color=VkKeyboardColor.SECONDARY)
        keyboard2.add_button('Показать избранное', color=VkKeyboardColor.SECONDARY)

        # Переменные для временного хранения результатов работы бота
        result_search = None
        result_user = None
        photos = None
        user_info = None

        webbrowser.open('https://vk.com/im?sel=-216099509')

        # Код работы бота
        for event in longpoll.listen():
            if user_info is not None:
                try:
                    vk_db.new_vk_user(user_info['id'],
                                      int(date.today().year - int(user_info['bdate'][-4:])), user_info['sex'],
                                      user_info['city']['id'])
                except err.UniqueViolation:
                    pass

            if event.type == VkEventType.MESSAGE_NEW:
                if user_info is None:
                    user_info = VK_data(token_program).get_user_data_only(event.user_id)
                if event.to_me:
                    request = event.text

                    # Команда "Привет"
                    if request in ("Привет", 'привет', "хай", 'Йоу'):
                        if user_info is not None:
                            try:
                                vk_db.new_vk_user(user_info['id'],
                                                  int(date.today().year - int(user_info['bdate'][-4:])),
                                                  user_info['sex'],
                                                  user_info['city']['id'])
                            except err.UniqueViolation:
                                pass
                        write_msg(event.user_id,
                                  f"Привет, {user_info['first_name']}!\n Хочешь с кем-нибудь познакомиться?",
                                  keyboard1.get_keyboard())

                    # Команда "Пока"
                    elif request in ("пока", 'нет', 'Нет'):
                        write_msg(event.user_id, "Пока((")
                        break
                    elif request in ("Поиск", 'да'):
                        result_search = VK_data(token_program).get_suitable(event.user_id)
                        write_msg(event.user_id,
                                  f"{user_info['first_name']}, я нашел для вас {len(result_search)}"
                                  f" кандидат{'ок' if user_info['sex'] == 2 else 'ов'}\n"
                                  f"Вот од{'на' if user_info['sex'] == 2 else 'ин'} из них:", keyboard2.get_keyboard())
                        result_user = result_search[randrange(0, len(result_search))]
                        photos = ','.join(VK_data(token_program).get_photos(result_user[2]))
                        write_msg(event.user_id,
                                  f'{result_user[0]} {result_user[1]}\nhttps://vk.com/id{result_user[2]}',
                                  keyboard2.get_keyboard())
                        paste_foto(event.user_id, photos, keyboard2.get_keyboard())

                    # Команда "Следующий"
                    elif request in ("Следующий", 'еще'):
                        try:
                            result_user = result_search[randrange(0, len(result_search))]
                            write_msg(event.user_id,
                                      f'{result_user[0]} {result_user[1]}\nhttps://vk.com/id{result_user[2]}',
                                      keyboard2.get_keyboard())
                            photos = ','.join(VK_data(token_program).get_photos(result_user[2]))
                            paste_foto(event.user_id, photos, keyboard2.get_keyboard())
                        except TypeError:
                            write_msg(event.user_id, 'Чтобы выбирать следующего, сначала нажмите "Поиск"',
                                      keyboard2.get_keyboard())

                    # Команда "Добавить в избранное"
                    elif request == "В избранное":
                        try:
                            try:
                                vk_db.favorites(result_user[2], result_user[0], result_user[1],
                                                f'https://vk.com/id{result_user[2]}', str(photos))
                                vk_db.fav_user(event.user_id, result_user[2])
                            except err.UniqueViolation:
                                pass
                            write_msg(event.user_id, "Добавлено!", keyboard2.get_keyboard())
                        except TypeError:
                            write_msg(event.user_id, 'Сначала нужно выбрать человека. Нажмите "Поиск"',
                                      keyboard2.get_keyboard())

                    # Команда "Показать избранное"
                    elif request == "Показать избранное":
                        list_of_fav = vk_db.get_fav_users(event.user_id)
                        count = 0
                        if len(list_of_fav) != 0:
                            write_msg(event.user_id,
                                      f'В вашем списке "Избранное" {len(list_of_fav)} человек.\n Вот они:',
                                      keyboard2.get_keyboard())
                            for fav in list_of_fav:
                                if count < 10:
                                    write_msg(event.user_id, f'{fav[0]} {fav[1]}\n{fav[2]}', keyboard2.get_keyboard())
                                    paste_foto(event.user_id, fav[3], keyboard2.get_keyboard())
                                    count += 1
                                else:
                                    time.sleep(1)
                                    write_msg(event.user_id, f'{fav[0]} {fav[1]}\n{fav[2]}', keyboard2.get_keyboard())
                                    paste_foto(event.user_id, fav[3], keyboard2.get_keyboard())
                                    count = 0
                        else:
                            write_msg(event.user_id, f'В вашем списке "Избранное" 0 человек.', keyboard2.get_keyboard())
                    else:
                        write_msg(event.user_id, "Не понял вашего запроса... Попробуйте команду на клавиатуре.",
                                  keyboard2.get_keyboard())
    except KeyboardInterrupt:
        exit('Программа принудительно завершена пользователем.')
