import configparser
from VKinder_db_engine import DatabaseConfig

config = configparser.ConfigParser()
config.read("base_settings.ini")

db_name = config["Database"]["db_name"]
user_name = config["Database"]["user_name"]
user_password = config["Database"]["user_password"]

new_db = DatabaseConfig(db_name, user_name, user_password)

if __name__ == '__main__':

    # # 0. Функция, удаляющая таблицы БД:
    # # def table_removal(table_name)
    #
    # new_db.table_removal('user_favorites')
    # new_db.table_removal('vk_user')
    # new_db.table_removal('favorites')


    # 1. Функция, создающая таблицы БД:
    # def table_creation(table_name, table_columns)

    # new_db.table_creation('vk_user', 'id SERIAL PRIMARY KEY, age INTEGER NOT NULL, gender VARCHAR(7) NOT NULL, city VARCHAR(40) NOT NULL')
    # new_db.table_creation('favorites', 'id SERIAL PRIMARY KEY, name VARCHAR(50), surname VARCHAR(50), profile_url VARCHAR(100) UNIQUE NOT NULL, photos VARCHAR(100)')
    # new_db.table_creation('user_favorites', 'id SERIAL PRIMARY KEY, vk_user_id INTEGER NOT NULL REFERENCES vk_user(id), fav_id INTEGER NOT NULL REFERENCES favorites(id)')


    # # 2. Функция, позволяющая добавить нового юзера
    # # def new_vk_user(age, gender, city)
    #
    # new_db.new_vk_user('30', 'Мужской', 'Москва')
    # new_db.new_vk_user('35', 'Мужской', 'Санкт-Петербург')
    # new_db.new_vk_user('20', 'Женский', 'Казань')

    # # 3. Функция, позволяющая изменить данные о клиенте
    # # def vk_user_editor(age, gender, city, id)
    #
    # new_db.vk_user_editor("21", "Женский", "Казань", "3")

    # # 4. Функция, позволяющая добавить в избранные новую запись.
    # # def favorites(name, surname, profile_url, photo_1_url, photo_2_url, photo_3_url)
    #
    # new_db.favorites('Регина', 'Плеханова', 'https://vk.com/regina_msk', 'photo100172_166443618,photo100172_166443618,photo100172_166443618')
    # new_db.favorites('Диана', 'Сухорукова', 'https://vk.com/id41347328', 'https://vk.com/id41347328?z=photo41347328_457245753%2Falbum41347328_0%2Frev')

    # # 5. Функция, позволяющая добавить связать запись в избранных с юзером.
    # # def fav_user(vk_user_id, fav_id)
    #
    # new_db.fav_user(1,1)
    # new_db.fav_user(1,3)
    # new_db.fav_user(2,1)

    # # 6. Функция, выводит список избранных юзера
    # # def get_fav_users(vk_user_id)
    # #
    # new_db.get_fav_users(1)


    # # 7. Функция, позволяющая удалить запись из таблицы по id
    # new_db.vk_user_removal('vk_user','3')

