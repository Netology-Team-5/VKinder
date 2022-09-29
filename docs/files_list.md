# Командный проект по курсу «Профессиональная работа с Python»

## VKinder - приложение для знакомств во Вконтакте

### Список файлов с описанием

1. [bot.py](https://github.com/Netology-Team-5/VKinder/blob/main/bot.py)
Скрипт, который работает с VK api, базой данных и общается с пользователем в VK.
- `def write_msg` - функция, позволяющая отвечать на сообщения юзера;
- `def paste_foto` - функция выводит фотографии подходящих людей под критерии поиска. 

2. [info_vk.py](https://github.com/Netology-Team-5/VKinder/blob/main/info_vk.py)
Класс с функциями для работы с API vk:
- `def get_user_data_only` - функция, возвращает параметры юзера для поиска.   
Если не указана дата рождения, то возраст рассчитывается как ср арифм возрастов друзей;
- `def average_friends_age` - функция, возвращает средний возраст друзей, если в профиле юзера не указана ГОД рождения;
- `def get_user_data_for_search` - функция, возвращает все параметры юзера для поиска;
- `def get_photos` - функция, возвращает 3 самые популярные фотографии подходящего человека;
- `def get_suitable` - функция, собирает информацию подходящих людей под критерии поиска:(Имя, Фамилия, URL)

4. [VKinder_db_engine.py](https://github.com/Netology-Team-5/VKinder/blob/main/VKinder_db_engine.py)
Класс с функциями для работы с базой данных:
- `def table_creation` - функция, создающая таблицы БД;
- `def table_removal` - функция, удаляющая таблицы БД;
- `def new_vk_user` - функция, позволяющая добавить нового юзера;
- `def vk_user_editor` - функция, позволяющая изменить данные о юзере;
- `def favorites` - функция, позволяющая добавить в избранные новую запись;
- `def fav_user` - функция, позволяющая связать запись в избранных с юзером;
- `def get_fav_users` - функция, выводит список избранных людей юзера; 
- `def vk_user_removal` - функция, позволяющая удалить запись из таблицы по id; 

5. [VKinder_db_input.py](https://github.com/Netology-Team-5/VKinder/blob/main/VKinder_db_input.py)
Скрипты для проверки и тестирования базы данных (создание, заполнение таблиц). 

6. [tokens.ini](https://github.com/Netology-Team-5/VKinder/blob/main/tokens.ini)
Токены для работы с API vk

7. [base_settings.ini](https://github.com/Netology-Team-5/VKinder/blob/main/base_settings.ini)
Ключи для работы с базой данных

8. [VKinder_db_v1.png](https://github.com/Netology-Team-5/VKinder/blob/main/VKinder_db_v1.png)
Схема базы данных 
