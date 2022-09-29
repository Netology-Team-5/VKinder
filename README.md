# Командный проект по курсу «Профессиональная работа с Python»

## VKinder - приложение для знакомств во Вконтакте

### Описание проекта

Программа-бот, которая выполняет следующие действия:
1. Используя информацию (возраст, пол, город) о пользователе, который общается с ботом в ВК, делает поиск других людей (других пользователей ВК) для знакомств.
2. У тех людей, которые подошли под критерии поиска, получает три самые популярные фотографии в профиле. Популярность определяется по количеству лайков.
3. Выводит в чат с ботом информацию о пользователе в формате:
```
Имя Фамилия
ссылка на профиль
три фотографии в виде attachment(https://dev.vk.com/method/messages.send)
```
4. Переходит к следующему человеку с помощью кнопки.
5. Сохраняет подходящих людей в список избранных.
6. Выводит список избранных людей.


### Зависимости
- python (3.4+)
- pip
- python-dev

### Документация
-[Как работать](https://github.com/Netology-Team-5/VKinder/blob/main/docs/how_to_start.md)
-[Список файлов с описанием](https://github.com/Netology-Team-5/VKinder/blob/main/docs/files_list.md)
