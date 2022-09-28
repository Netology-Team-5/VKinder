import requests
from datetime import datetime
import configparser
from pprint import pprint


config = configparser.ConfigParser()
config.read("tokens.ini")
token_program = config['TOKEN_SEARCH']['token']


class VK_data:
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

    def average_friends_age(self, user_id):
        """ Средний возраст друзей если
        в моем профиле не указана ГОД родждения"""

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

    def get_user_data_only(self, user_ids):
        """ Формирование параметров для поиска. Если не указана дата рождения,
        то возраст рассчитывается как ср арифм возростов друзей """

        json_params = {
            'user_ids': user_ids,
            'fields': 'bdate, city, sex'
        }
        user_data = requests.get(url=self.users_get_url,
                                 params={**self.params, **json_params}).json()['response'][0]
        return user_data

    def get_user_data_for_search(self, user_ids):
        """ Формирование параметров для поиска. Если не указана дата рождения,
        то возраст рассчитывается как ср арифм возростов друзей """

        json_params = {
            'user_ids': user_ids,
            'fields': 'bdate, city, sex'
        }
        user_data = requests.get(url=self.users_get_url,
                                 params={**self.params, **json_params}).json()['response'][0]
        sex = user_data['sex']
        if sex == 1:
            sex = 2
        if sex == 2:
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

    def get_photos(self, owner_id):
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

    def get_suitable(self, user_id):
        """ Сбор информации по подходящим людям:
        Имя, Фамилия, урлы фотографий и лайки к ним """

        json_params = {
            'fields': 'is_friend, is_closed, has_photo',
            'birth_month': 1,
        }

        searcher_data = str(self.get_user_data_for_search(user_id)).strip('{}')
        vk_code = 'var thirteen_thousand_users = [];' \
                  'var month = 1;' \
                  'while (month < 13) {' \
                  'var users = API.users.search({"fields:"is_friend,is_closed,has_photo","birth_month":month,' + \
                  searcher_data + '});' \
                  'thirteen_thousand_users = thirteen_thousand_users + users;' \
                  'month = month + 1;};' \
                  'return thirteen_thousand_users;'
        user_info = []
        thirteen_thousand_users = requests.get(url=self.execute_url, params={**self.params, 'code': vk_code}).json()
        for item in thirteen_thousand_users:
            if item['is_friend'] == 0 and item['has_photo'] == 1 and item['is_closed'] is False:
                first_name = item['first_name']
                last_name = item['last_name']
                user_link = item['id']
                user_info.append((first_name, last_name, user_link))
        return user_info


if __name__ == '__main__':
    # pprint(my_data.get_user_data(265887656))
    # pprint(my_data.get_user_data(328892096))

    # pprint(VK_data(token_program).get_photos(39291361))
    # pprint(VK_data(token_program).get_photos(328892096))

    # pprint(VK_data(token_program).get_photos(1058441))
    # pprint(VK_data(token_program).get_user_data_only(1058441))
    # pprint(VK_data(token_program).get_suitable(328892096))
    # pprint(VK_data(token_program).get_photos(1058441))
    pprint(VK_data(token_program).get_suitable(328892096))
