import configparser
import webbrowser

import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.vk_api import VkApi
from get_code import get_token_vk

from main import Vk

client_secret = 'ggCUOCDSncOBNQbiGtDb'
app_id = '51432598'

config = configparser.ConfigParser()
config.read("tokens.ini")

vk_program_apitoken = config['TOKEN_BOT']['token']
token_program = get_token_vk()
token_program = config['TOKEN_SEARCH']['token']

vk_enter = vk_api.VkApi(token=vk_program_apitoken)
vk = vk_enter.get_api()
longpoll = VkLongPoll(vk_enter)

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('Следующий', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('В избранное', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Показать избранное', color=VkKeyboardColor.SECONDARY)


def write_msg(user_id, message, *keyboard):
    vk.messages.send(keyboard=keyboard, user_id=user_id, message=message, random_id=randrange(10 ** 7))


def paste_foto(user_id, attachment, *keyboard):
    vk.messages.send(keyboard=keyboard, user_id=user_id, attachment=attachment, random_id=randrange(10 ** 7))


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            user_info = vk.users.get(user_ids=event.user_id, fields='sex, bdate, city')

            if request == "привет":
                write_msg(event.user_id, f"Привет, {user_info[0]['first_name']}!\n Хочешь с кем-нибудь познакомиться?",
                          keyboard.get_keyboard())
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request in ("Поиск", 'да', "Следующий", 'еще'):
                result_search = Vk(token_program, str(event.user_id)).users_search(user_id=str(event.user_id))
                result_user = Vk(token_program, str(event.user_id)).user_info(*result_search)
                write_msg(event.user_id, result_user[0], keyboard.get_keyboard())
                if isinstance(result_user, tuple):
                    paste_foto(event.user_id, result_user[1], keyboard.get_keyboard())
            elif request == "В избранное":
                write_msg(event.user_id, "Пока что я не умею сохранять в избранное", keyboard.get_keyboard())
            elif request == "Показать избранное":
                write_msg(event.user_id, "Пока что я не умею показывать избранное", keyboard.get_keyboard())
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...", keyboard.get_keyboard())
