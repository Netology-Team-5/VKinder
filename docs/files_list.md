# Командный проект по курсу «Профессиональная работа с Python»

## VKinder - приложение для знакомств во Вконтакте

### Список файлов с описанием

1. [bot.py](https://github.com/Netology-Team-5/VKinder/blob/main/bot.py)
Скрипт, который работает с VK api, базой данных и общается с пользователем в VK.
   - `write_msg` - функция, позволяющая отвечать на сообщения юзера;
   - `paste_foto` - функция выводит фотографии подходящих людей под критерии поиска. 

2. [info_vk.py](https://github.com/Netology-Team-5/VKinder/blob/main/info_vk.py)
Класс с функциями для работы с API vk:
   - `get_user_data_only` - функция возвращает параметры юзера для поиска.   
   Если не указана дата рождения, то возраст рассчитывается как ср арифм возрастов друзей;
   - `average_friends_age` - функция возвращает средний возраст друзей, если в профиле юзера не указана ГОД рождения;
   - `get_user_data_for_search` - функция возвращает все параметры юзера для поиска;
   - `get_photos` - функция возвращает 3 самые популярные фотографии подходящего человека;
   - `get_suitable` - функция собирает информацию подходящих людей под критерии поиска:(Имя, Фамилия, URL)
   - `blacklist_cleaner` - функция удаляет из результатов поиска профили из черного списка.

3. [VKinder_db_engine.py](https://github.com/Netology-Team-5/VKinder/blob/main/VKinder_db_engine.py)
Класс с функциями для работы с базой данных:
   - `table_creation` - функция, создающая таблицы БД;
   - `table_removal` - функция, удаляющая таблицы БД;
   - `new_vk_user` - функция, позволяющая добавить нового юзера;
   - `vk_user_editor` - функция, позволяющая изменить данные о юзере;
   - `favorites` - функция, позволяющая добавить в избранные новую запись;
   - `fav_user` - функция, позволяющая связать запись в избранных с юзером;
   - `get_fav_users` - функция, выводит список избранных людей юзера; 
   - `vk_user_removal` - функция, позволяющая удалить запись из таблицы по id; 

4. [get_code.py](https://github.com/Netology-Team-5/VKinder/blob/main/get_code.py)
Модуль запроса токена, в случае его отсутствия у пользователя.
   - `get_token_vk` - функция запускает драйвер браузера для получения кода и сохраняет его в переменную. 

5. [tokens.ini](https://github.com/Netology-Team-5/VKinder/blob/main/tokens.ini)
Токены для работы с API vk

6. [base_settings.ini](https://github.com/Netology-Team-5/VKinder/blob/main/base_settings.ini)
Ключи для работы с базой данных

7. [VKinder_db_v1.png](https://github.com/Netology-Team-5/VKinder/blob/main/VKinder_db_v1.png)
Схема базы данных 
