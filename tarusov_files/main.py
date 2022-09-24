import configparser
import random
from datetime import date

import vk_api


class Vk:

    def __init__(self, token: str, login: str):
        self.token = token
        self.vk_session = vk_api.VkApi(login=login, token=self.token)
        self.vk_session.auth(token_only=True)
        self.vk = self.vk_session.get_api()

    def users_search(self, user_id):
        user_data = self.vk.users.get(user_ids=user_id, fields='sex, bdate, city', access_token=self.token)
        user_city = user_data[0]["city"]["id"] if user_data[0]["city"]["id"] else None
        searched_sex = 1 if user_data[0]['sex'] == 2 else 2
        user_age = date.today().year - int(user_data[0]['bdate'][-4:])
        age_from = user_age - 5
        age_to = user_age + 5
        search_result = self.vk.users.search(count=1000, fields='sex, city, is_friend',
                                             city=user_city, sex=searched_sex, age_from=age_from, age_to=age_to,
                                             access_token=self.token)
        result = []
        for person in search_result['items']:
            if 'city' in person and person['is_friend'] == 0 and person['city'] == user_data[0]['city'] and \
                    person['is_closed'] is False:
                result.append(person)
        lenresult = len(result)
        return result, lenresult

    def user_info(self, result, lenresult):
        user = result[random.randrange(0, lenresult)]
        name = user['first_name']
        last_name = user['last_name']
        profile_link = f'https://vk.com/id{user["id"]}'
        try:
            get_photos = self.vk.photos.get(owner_id=user['id'], album_id='profile', extended=1,
                                            access_token=self.token)
            if len(get_photos['items']) > 3:
                ranking_photos = sorted(get_photos['items'], key=lambda x: x['likes']['count'], reverse=True)
                result_photos_list = [f'photo{user["id"]}_{photo["id"]}' for photo in ranking_photos[3:]]
                result_user = (f'{name} {last_name}\n{profile_link}\n', ','.join(result_photos_list))
            else:
                result_photo_list = [f'photo{user["id"]}_{photo["id"]}' for photo in get_photos['items']]
                result_user = (f'{name}\n{last_name}\n{profile_link}\n', ','.join(result_photo_list))
        except vk_api.exceptions.ApiError:
            result_user = f'{name} {last_name}\n{profile_link}\nУ этого человка закрытый доступ к фото или его нет.'
        return result_user


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("tokens.ini")
    access_token = config['TOKEN_SEARCH']['token']
    user_id = '7451160'
    vk = Vk(access_token, user_id)
    print(vk.user_info(*vk.users_search(user_id)))
