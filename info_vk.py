"""Модуль работы с API vk.com через Standalone-приложение.

класс VK_data содержит методы для работы API VK;
метод average_friends_age возвращает средний возраст друзей;
метод get_user_data_only возвращает словарь с параметрами юзера;
метод get_user_data_for_search возвращает словарь с параметрами юзера, нужными для выполнения поиска;
метод get_photos возвращает фотографии найденного профиля;
метод get_suitable возвращает информацию о подходящих профилях.
"""

import configparser
import requests
from datetime import datetime


class VK_data:
    """Содержит методы для работы API VK через Standalone-приложение."""

    users_get_url = 'https://api.vk.com/method/users.get'
    users_search_url = 'https://api.vk.com/method/users.search'
    friends_get_url = 'https://api.vk.com/method/friends.get'
    photos_get_url = 'https://api.vk.com/method/photos.get'
    execute_url = 'https://api.vk.com/method/execute'

    def __init__(self, vk_token):
        self.params = {
            'access_token': vk_token,
            'v': '5.131'
        }

    def average_friends_age(self, user_id: int) -> int:
        """Возвращает средний возраст друзей, если в профиле юзера не указана год рождения."""
        json_params = {
            'user_id': user_id,
            'order': 'hints',
            'count': 15,
            'fields': 'bdate'
        }
        friends = requests.get(url=self.friends_get_url,
                               params={**self.params, **json_params}).json()['response']['items']
        friends_age_list = [datetime.now().year - datetime.strptime(item['bdate'], "%d.%m.%Y").year
                            for item in friends if 'bdate' in item if len(item['bdate']) >= 8]
        average_age = int(sum(friends_age_list) / len(friends_age_list))
        return average_age

    def get_user_data_only(self, user_ids: int) -> dict:
        """Возвращает словарь с параметрами юзера.

         В словаре: id, дата рождения, город, пол, имя, фамилия, статус профиля: открыт/закрыт.
         """
        json_params = {
            'user_ids': user_ids,
            'fields': 'bdate, city, sex'
        }
        user_data = requests.get(url=self.users_get_url,
                                 params={**self.params, **json_params}).json()['response'][0]
        return user_data

    def get_user_data_for_search(self, user_ids: int) -> dict:
        """Возвращает словарь с параметрами юзера, нужными для выполнения поиска методом get_suitable.

         В словаре: минимальный возраст поиска, максимальный возраст поиска, город, пол.
         """
        json_params = {
            'user_ids': user_ids,
            'fields': 'bdate, city, sex'
        }
        user_data = requests.get(url=self.users_get_url,
                                 params={**self.params, **json_params}).json()['response'][0]
        sex = user_data['sex']
        if sex == 1:
            sex = 2
        elif sex == 2:
            sex = 1
        city = user_data['city']['id']
        if 'bdate' in user_data:
            if len(user_data['bdate']) >= 8:
                age = datetime.now().year - datetime.strptime(user_data['bdate'], "%d.%m.%Y").year
            else:
                age = self.average_friends_age(user_ids)
        else:
            age = self.average_friends_age(user_ids)
        age_from = age - 10
        age_to = age + 0
        my_params = {'sex': sex, 'age_from': age_from, 'age_to': age_to, 'city': city}
        return my_params

    def get_photos(self, owner_id: int) -> list:
        """Возвращает максимум три фотографии с наибольшим количеством лайков у найденного профиля"""
        json_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1,
            'offset': 0
        }
        try:
            photos_json = requests.get(self.photos_get_url,
                                       params={**self.params, **json_params}).json()['response']
            count_all_photos = photos_json['count']
            all_photos_json_list = photos_json['items']
            while len(all_photos_json_list) < count_all_photos:
                json_params['offset'] += 50
                new_array_photos = (requests.get(self.photos_get_url,
                                                 params={**self.params, **json_params}).json()['response'])['items']
                all_photos_json_list += new_array_photos
        except KeyError:
            pass
        else:
            photos = [(item['likes']['count'], f"photo{item['owner_id']}_{item['id']}")
                      for item in all_photos_json_list]
            photos = sorted(photos, reverse=True)
            photos = [item[1] for item in photos][:3]
            return photos

    def get_suitable(self, user_id: int) -> list:
        """Возвращает информацию о подходящих под параметры поиска профилях.


        :return: список кортежей, содержащих имя, фамилию и id найденного профиля.
        """
        searcher_data = str(self.get_user_data_for_search(user_id)).strip('{}').replace("'", '"')
        # Скрипт в формате VKscript для метода API execute.
        vk_code = 'var month, thirteen_thousand_users, users;' \
                  'thirteen_thousand_users = [];' \
                  'month = 1;' \
                  'while (month < 13) {' \
                  '    users = API.users.search({"count": 1000, "fields": "is_friend,is_closed,has_photo", ' \
                  '"birth_month": month, ' + searcher_data + '}).items;' \
                  '    thirteen_thousand_users = thirteen_thousand_users + users;' \
                  '    month = month + 1;' \
                  '};' \
                  'return thirteen_thousand_users;'
        thirteen_thousand_users = \
            requests.get(url=self.execute_url, params={**self.params, 'code': vk_code}).json()['response']

        user_info = []
        for item in thirteen_thousand_users:
            if item['is_friend'] == 0 and item['has_photo'] == 1 and item['is_closed'] is False:
                first_name = item['first_name']
                last_name = item['last_name']
                user_link = item['id']
                user_info.append((first_name, last_name, user_link))

        return user_info


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("tokens.ini")
    token_program = config['TOKEN_SEARCH']['token']
