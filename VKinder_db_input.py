"""Скрипты для проверки и тестирования базы данных (создание, заполнение таблиц)."""
import configparser

from VKinder_db_engine import DatabaseConfig

config = configparser.ConfigParser()
config.read("base_settings.ini")

db_name = config["Database"]["db_name"]
user_name = config["Database"]["user_name"]
user_password = config["Database"]["user_password"]

new_db = DatabaseConfig(db_name, user_name, user_password)

if __name__ == '__main__':

    # 0. Скрипты, удаляющие таблицу БД:
    # new_db.table_removal('user_favorites')
    # new_db.table_removal('vk_user')
    # new_db.table_removal('favorites')

    # 1. Скрипты, создающие таблицы БД:
    # new_db.table_creation('vk_user', 'user_id_in_vk INTEGER PRIMARY KEY, '
    #                                  '          age INTEGER NOT NULL, '
    #                                  '       gender INTEGER NOT NULL, '
    #                                  '         city INTEGER NOT NULL')
    # new_db.table_creation('favorites', ' vk_user_id INTEGER PRIMARY KEY, '
    #                                    '       name VARCHAR(50), '
    #                                    '    surname VARCHAR(50), '
    #                                    'profile_url VARCHAR(100) UNIQUE NOT NULL, '
    #                                    '     photos VARCHAR(100)')
    # new_db.table_creation('user_favorites', '           id SERIAL PRIMARY KEY, '
    #                                         'user_id_in_vk INTEGER NOT NULL REFERENCES vk_user(user_id_in_vk), '
    #                                         '       fav_id INTEGER NOT NULL REFERENCES favorites(vk_user_id)')

    # 2. Скрипты, позволяющие добавить нового юзера
    # new_db.new_vk_user('30', 'Мужской', 'Москва')
    # new_db.new_vk_user('35', 'Мужской', 'Санкт-Петербург')
    # new_db.new_vk_user('20', 'Женский', 'Казань')

    # 3. Скрипты, позволяющие изменить данные о клиенте
    # new_db.vk_user_editor("21", "Женский", "Казань", "3")

    # 4. Скрипты, позволяющие добавить в избранные новую запись.
    # new_db.favorites('Регина', 'Плеханова', 'https://vk.com/regina_msk', 'photo100172_166443618,photo100172_166443618,photo100172_166443618')
    # new_db.favorites('Диана', 'Сухорукова', 'https://vk.com/id41347328', 'https://vk.com/id41347328?z=photo41347328_457245753%2Falbum41347328_0%2Frev')

    # 5. Скрипты, позволяющие связать запись в избранных с юзером.
    # new_db.fav_user(1,1)
    # new_db.fav_user(1,3)
    # new_db.fav_user(2,1)

    # 6. Скрипты, выводящие список избранных юзера
    # new_db.get_fav_users(7451160)

    # 7. Скрипты, позволяющие удалить запись из таблицы по id
    # new_db.vk_user_removal('vk_user','3')
    # new_db.vk_user_removal('user_favorites', '4')

    # 8. Скрипт, позволяющий очистить содержимое избранного
    new_db.clear_favorites_table()



    # 8. Скрипты, вызывающие blacklist
    # print(new_db.get_user_blacklist(7451160))

