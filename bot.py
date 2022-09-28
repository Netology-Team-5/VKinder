import configparser
import vk_api
import time
from random import randrange
from datetime import date
from psycopg2 import errors as err
import webbrowser
from selenium.common import exceptions
from sys import exit

import get_code
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from info_vk import VK_data
from VKinder_db_engine import DatabaseConfig


def write_msg(user_id, message, *keyboard):
    vk.messages.send(keyboard=keyboard, user_id=user_id, message=message, random_id=randrange(10 ** 9))


def paste_foto(user_id, attachment, *keyboard):
    vk.messages.send(keyboard=keyboard, user_id=user_id, attachment=attachment, random_id=randrange(10 ** 9))


if __name__ == '__main__':

    config = configparser.ConfigParser()

    config.read("tokens.ini")
    vk_api_token = config['TOKEN_BOT']['token']
    if config['TOKEN_SEARCH']['token'] == '':
        try:
            token_program = get_code.get_token_vk()
        except exceptions.NoSuchWindowException:
            exit('Запустите программу заново и введите ключ авторизации корректно: либо в браузере, либо в файле tokens.ini')

    else:
        token_program = config['TOKEN_SEARCH']['token']

    config.read("base_settings.ini")
    db_name = config["Database"]["db_name"]
    user_name = config["Database"]["user_name"]
    user_password = config["Database"]["user_password"]

    vk_db = DatabaseConfig(db_name, user_name, user_password)
    vk_db.table_creation('vk_user', 'user_id_in_vk INTEGER PRIMARY KEY NOT NULL, age INTEGER NOT NULL, '
                                    'gender INTEGER NOT NULL, city INTEGER NOT NULL')
    vk_db.table_creation('favorites', 'vk_user_id INTEGER PRIMARY KEY, name VARCHAR(50), surname VARCHAR(50), '
                                      'profile_url VARCHAR(100) UNIQUE NOT NULL, photos VARCHAR(100)')
    vk_db.table_creation('user_favorites', 'id SERIAL PRIMARY KEY, '
                                           'user_id_in_vk INTEGER NOT NULL REFERENCES vk_user(user_id_in_vk), '
                                           'fav_id INTEGER NOT NULL REFERENCES favorites(vk_user_id)')

    vk_enter = vk_api.VkApi(token=vk_api_token)
    vk = vk_enter.get_api()
    longpoll = VkLongPoll(vk_enter)

    keyboard1 = VkKeyboard(one_time=True)
    keyboard1.add_button('Поиск', color=VkKeyboardColor.PRIMARY)

    keyboard2 = VkKeyboard(one_time=True)
    keyboard2.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
    keyboard2.add_button('Следующий', color=VkKeyboardColor.PRIMARY)
    keyboard2.add_line()
    keyboard2.add_button('В избранное', color=VkKeyboardColor.SECONDARY)
    keyboard2.add_button('Показать избранное', color=VkKeyboardColor.SECONDARY)

    result_search = None
    result_user = None
    photos = None
    user_info = None

    webbrowser.open('https://vk.com/im?sel=-216099509')

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
                user_info = VK_data(token_program).get_user_data_only(str(event.user_id))
            if event.to_me:
                request = event.text
                if request in ("Привет", 'привет', "хай", 'Йоу'):
                    if user_info is not None:
                        try:
                            vk_db.new_vk_user(user_info['id'],
                                              int(date.today().year - int(user_info['bdate'][-4:])), user_info['sex'],
                                              user_info['city']['id'])
                        except err.UniqueViolation:
                            pass
                    write_msg(event.user_id,
                              f"Привет, {user_info['first_name']}!\n Хочешь с кем-нибудь познакомиться?",
                              keyboard1.get_keyboard())
                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                    break
                elif request in ("Поиск", 'да'):
                    result_search = VK_data(token_program).get_suitable(str(event.user_id))
                    write_msg(event.user_id,
                              f"{user_info['first_name']}, я нашел для вас {len(result_search)}"
                              f" кандидат{'ок' if user_info['sex'] == 2 else 'ов'}\n"
                              f"Вот од{'на' if user_info['sex'] == 2 else 'ин'} из них:", keyboard2.get_keyboard())
                    result_user = result_search[randrange(0, len(result_search))]
                    photos = ','.join(VK_data(token_program).get_photos(str(result_user[2])))
                    write_msg(event.user_id,
                              f'{result_user[0]} {result_user[1]}\nhttps://vk.com/id{result_user[2]}',
                              keyboard2.get_keyboard())
                    paste_foto(event.user_id, VK_data(token_program).get_photos(str(result_user[2])),
                               keyboard2.get_keyboard())
                elif request in ("Следующий", 'еще'):
                    try:
                        result_user = result_search[randrange(0, len(result_search))]
                        write_msg(event.user_id,
                                  f'{result_user[0]} {result_user[1]}\nhttps://vk.com/id{result_user[2]}',
                                  keyboard2.get_keyboard())
                        photos = ','.join(VK_data(token_program).get_photos(str(result_user[2])))
                        paste_foto(event.user_id, VK_data(token_program).get_photos(str(result_user[2])),
                                   keyboard2.get_keyboard())
                    except TypeError:
                        write_msg(event.user_id, 'Чтобы выбирать следующего, сначала нажмите "Поиск"',
                                  keyboard2.get_keyboard())
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
                elif request == "Показать избранное":
                    list_of_fav = vk_db.get_fav_users(event.user_id)
                    count = 0
                    write_msg(event.user_id, f'Вашем списки "Избранное" {len(list_of_fav)} человек.\n Вот они:',
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
                    write_msg(event.user_id, "Не понял вашего запроса... Попробуйте команду на клавиатуре.",
                              keyboard2.get_keyboard())
