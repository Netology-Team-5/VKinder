"""Модуль работы с базой данных PostgreSQL.

класс DatabaseConfig содержит методы для для создания и работы c базой данных;
метод load_connection_info создает словарь параметров СУБД;
метод create_db подключает к СУБД и создание новой базы данных;
метод table_creation создает таблицы;
метод table_removal удаляет таблицы;
метод new_vk_user добавляет нового пользователя в таблицу;
метод vk_user_editor изменяет данные пользователя в таблице;
метод favorites добавляет в таблицу favorites новую запись;
метод get_fav_users возвращает список избранных профилей пользователя;
метод vk_user_removal удаляет запись по id пользователя;
"""
import psycopg2
from configparser import ConfigParser
from typing import Dict


class DatabaseConfig:
    """Содержит методы для работы с базой данных PostgreSQL."""

    def __init__(self, database: str, user: str, password: str):
        """Получает название базы данных, пользователя базы данных и пароля для подключения."""
        self.database = database
        self.user = user
        self.password = password

    @staticmethod
    def load_connection_info(ini_filename: str) -> Dict[str, str]:
        """Создание словаря параметров СУБД из файла .ini"""

        parser = ConfigParser()
        parser.read(ini_filename)
        con_info = {param[0]: param[1] for param in parser.items("Database")}
        return con_info

    @staticmethod
    def create_db(con_info: Dict[str, str], ) -> None:
        """Подключение к СУБД и создание новой базы данных"""

        psql_connection_string = f"user={con_info['user_name']} password={con_info['user_password']}"
        conn = psycopg2.connect(psql_connection_string)
        cur = conn.cursor()
        conn.autocommit = True
        sql_query = f"CREATE DATABASE {con_info['db_name']}"
        try:
            cur.execute(sql_query)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
            print(f"Query: {cur.query}")
            cur.close()
        else:
            conn.autocommit = False

    def table_creation(self, table_name: str, table_columns: str):
        """Создает таблицы в базе данных."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} ({table_columns});""")
            conn.commit()
        conn.close()

    def table_removal(self, table_name: str):
        """Удаляет таблицы из базы данных."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(f"""DROP TABLE {table_name};""")
            conn.commit()
        conn.close()

    def new_vk_user(self, user_id_in_vk: int, age: int, gender: int, city: int):
        """Добавляет нового пользователя в таблицу vk_user."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO vk_user(user_id_in_vk, age, gender, city) VALUES (%s, %s, %s, %s);""",
                        (user_id_in_vk, age, gender, city))
            conn.commit()
        conn.close()

    def vk_user_editor(self, age: int, gender: int, city: int, user_id: int):
        """Изменяет данные пользователя в таблице vk_user."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""UPDATE vk_user SET age = %s, gender = %s, city = %s WHERE id = %s;""",
                        (age, gender, city, user_id))
            conn.commit()
        conn.close()

    def favorites(self, vk_user_id: int, name: str, surname: str, profile_url: str, photos: str):
        """Добавляет в таблицу favorites новую запись."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO favorites(vk_user_id, name, surname, profile_url, photos) 
                VALUES (%s, %s, %s, %s, %s);""",
                (vk_user_id, name, surname, profile_url, photos))
            conn.commit()
        conn.close()

    def fav_user(self, user_id_in_vk: int, fav_id: int):
        """Связывает запись в favorites и vk_user через таблицу user_favorites."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO user_favorites(user_id_in_vk, fav_id) VALUES (%s, %s);""",
                        (user_id_in_vk, fav_id))
            conn.commit()
        conn.close()

    def user_blacklist(self, user_id_in_vk: int, blk_id: int):
        """Добавляет в user_blacklist новую запись."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO user_blacklist(user_id_in_vk, blk_id) VALUES (%s, %s);""",
                        (user_id_in_vk, blk_id))
            conn.commit()
        conn.close()

    def get_fav_users(self, user_id_in_vk: int) -> list:
        """Возвращает список избранных профилей пользователя.

        :return список кортежей, содержащих id профиля, имя, фамилию, фотографии.
        """
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT name, surname, profile_url, photos FROM user_favorites uf 
                LEFT JOIN favorites f ON uf.fav_id = f.vk_user_id
                WHERE user_id_in_vk = %s;       
            """, (user_id_in_vk,))
            return cur.fetchall()

    def get_user_blacklist(self, user_id_in_vk: int) -> list:
        """Возвращает список профилей из черного списка пользователя.

        :return список id профилей, находящихся в черном списке.
        """
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT blk_id FROM user_blacklist
                WHERE user_id_in_vk = %s;       
            """, (user_id_in_vk,))
            result = [item[0] for item in cur.fetchall()]
            return result

    def vk_user_removal(self, table: str, id_user: int):
        """Удаляет запись из таблицы по id пользователя."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(f"""DELETE FROM {table} WHERE id=%s;""", id_user)
            conn.commit()
        conn.close()

    def clear_favorites_table(self):
        """Очищает таблицу избранного."""
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(f"""DELETE FROM user_favorites;
                            DELETE FROM favorites;""")
            conn.commit()
        conn.close()
