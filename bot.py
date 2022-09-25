import configparser
import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
# from vk_api.vk_api import VkApi
# from get_code import get_token_vk

from info_vk import VK_data

config = configparser.ConfigParser()
config.read("tokens.ini")

vk_program_apitoken = config['TOKEN_BOT']['token']

# get_token_vk() - это получение токена через селениум
# token_program = get_token_vk()

# config['TOKEN_SEARCH']['token'] - для известного токена
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

            if request in ("Привет", 'привет', "хай", 'Йоу'):
                write_msg(event.user_id, f"Привет, {user_info[0]['first_name']}!\n Хочешь с кем-нибудь познакомиться?",
                          keyboard.get_keyboard())
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request in ("Поиск", 'да', "Следующий", 'еще'):
                result_search = VK_data(token_program).get_suitable(VK_data(token_program).get_user_data(str(event.user_id)))
                result_user = result_search[randrange(0, len(result_search))]
                write_msg(event.user_id, f'{result_user[0]} {result_user[1]}\nhttps://vk.com/id{result_user[2]}', keyboard.get_keyboard())
                # if isinstance(result_user, tuple):
                write_msg(event.user_id, VK_data(token_program).get_photos(str(event.user_id)), keyboard.get_keyboard())
            elif request == "В избранное":
                write_msg(event.user_id, "Пока что я не умею сохранять в избранное", keyboard.get_keyboard())
            elif request == "Показать избранное":
                write_msg(event.user_id, "Пока что я не умею показывать избранное", keyboard.get_keyboard())
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...", keyboard.get_keyboard())
