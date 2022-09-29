# Командный проект по курсу «Профессиональная работа с Python»

## VKinder - приложение для знакомств во Вконтакте

### Как работать с проложением.

1. Установить PostgreSQL. 

2. Установить базу данных через терминал командой:
```
createbd -U логин имя_бд
По умочанию логин:postgres, имя_бд: VKinder
createbd -U postgres VKinder
```

4. В файле [base_settings.ini](https://github.com/Netology-Team-5/VKinder/blob/main/base_settings.ini) прописать:
- Имя бд к `db_name`(по умолчанию `= VKinder`);
- Логин postgres к `user_name`(по умолчание `postgres`);
- Пароль postgres к `user_password`.

4. В файле [tokens.ini](https://github.com/Netology-Team-5/VKinder/blob/main/tokens.ini) прописать токен к VK.
- Сгенерировать личный ключ по [ссылке](https://oauth.vk.com/oauth/authorize?client_id=51432598&scope=65536&redirect_uri=https://vk.com/im?media%3D&sel=-216114574&display=popup&response_type=token&slogin_h=9a90a048692bb5042b.5b693fa27bae8d0d3a&__q_hash=a744e6552469a618bf825b408b432d41) 
- В `[TOKEN_SEARCH]` добавить личный ключ
- В `[TOKEN_BOT]` лежит ключ на группу. Его трогать не надо. 

5. Запустить [бота](https://github.com/Netology-Team-5/VKinder/blob/main/bot.py).

6. Войти в личный чат группы [Team5 VKinder](https://vk.com/im?sel=-216099509)
7. Написать сообщение "Привет" 
9. Нажать на кнопку Поиск. 
- Бот выведет на экран подходящего под критерии поиска человека. 

Кнопки:
- `Поиск` - программа выполнит новый поиск.  
Имеет смысл повторно нажимать, чтобы в выборку попали новые пользователи, которых не было на момент выполнения первого поиска.

- `Следующий` - выведет на экран, следующего человека, подходящего под критерии поиска.

- `В избранное` - добавит текущего на экране человека в подборку "Избранное"

- `Показать избранное` - выведет на экран поочередно, всех людей, которых добавили в "Избранное"

