import configparser
import vk_api
from random import randrange
from datetime import date
from psycopg2 import errors as err
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from info_vk import VK_data
from VKinder_db_engine import DatabaseConfig

config = configparser.ConfigParser()

config.read("tokens.ini")
vk_api_token = config['TOKEN_BOT']['token']
token_program = config['TOKEN_SEARCH']['token']

config.read("base_settings.ini")
db_name = config["Database"]["db_name"]
user_name = config["Database"]["user_name"]
user_password = config["Database"]["user_password"]

vk_db = DatabaseConfig(db_name, user_name, user_password)

vk_enter = vk_api.VkApi(token=vk_api_token)
vk = vk_enter.get_api()
longpoll = VkLongPoll(vk_enter)

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('Следующий', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('В избранное', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Показать избранное', color=VkKeyboardColor.SECONDARY)


def write_msg(user_id, message, *keyboard):
    vk.messages.send(keyboard=keyboard, user_id=user_id, message=message, random_id=randrange(10 ** 9))


def paste_foto(user_id, attachment, *keyboard):
    vk.messages.send(keyboard=keyboard, user_id=user_id, attachment=attachment, random_id=randrange(10 ** 9))


result_user = None
photos = None
user_info = None
for event in longpoll.listen():
    if user_info is not None:
        try:
            vk_db.new_vk_user(user_info['id'],
                              int(date.today().year - int(user_info['bdate'][-4:])), user_info['sex'],
                              user_info['city']['id'])
        except err.UniqueViolation:
            pass
    if event.type == VkEventType.MESSAGE_NEW:
        user_info = VK_data(token_program).get_user_data_only(str(event.user_id))
        if event.to_me:
            request = event.text
            if request in ("Привет", 'привет', "хай", 'Йоу'):
                write_msg(event.user_id,
                          f"Привет, {user_info['first_name']}!\n Хочешь с кем-нибудь познакомиться?",
                          keyboard.get_keyboard())
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request in ("Поиск", 'да', "Следующий", 'еще'):
                result_search = VK_data(token_program).get_suitable(str(event.user_id))
                result_user = result_search[randrange(0, len(result_search))]
                photos = ','.join(VK_data(token_program).get_photos(str(result_user[2])))
                write_msg(event.user_id,
                          f'{result_user[0]} {result_user[1]}\nhttps://vk.com/id{result_user[2]}', keyboard.get_keyboard())
                paste_foto(event.user_id, photos, keyboard.get_keyboard())
            elif request == "В избранное":
                try:
                    vk_db.favorites(result_user[2], result_user[0], result_user[1], f'https://vk.com/id{result_user[2]}', str(photos))
                    vk_db.fav_user(event.user_id, result_user[2])
                except err.UniqueViolation:
                    pass
                write_msg(event.user_id, "Добавлено!", keyboard.get_keyboard())
            elif request == "Показать избранное":
                list_of_fav = vk_db.get_fav_users(event.user_id)
                # вызывает функцию, которая дает список избранных
                for fav in list_of_fav:
                    write_msg(event.user_id, f'{fav[0]} {fav[1]}\n{fav[2]}', keyboard.get_keyboard())
                    photos = fav[3]
                    list_p = photos
                    paste_foto(event.user_id, f'{photos}', keyboard.get_keyboard())
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...", keyboard.get_keyboard())
