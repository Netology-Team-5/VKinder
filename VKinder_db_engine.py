import psycopg2


class DatabaseConfig:
    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password

    def table_creation(self, table_name, table_columns):
        # 1. Функция, создающая таблицы БД:
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} ({table_columns});""")
            conn.commit()
        conn.close()

    def table_removal(self, table_name):
        # Функция, удаляющая таблицы БД:
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(f"""DROP TABLE {table_name};""")
            conn.commit()
        conn.close()

    def new_vk_user(self, user_id_in_vk, age, gender, city):
        # 2. Функция, позволяющая добавить нового юзера
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO vk_user(user_id_in_vk, age, gender, city) VALUES (%s, %s, %s, %s);""", (user_id_in_vk, age, gender, city))
            conn.commit()
        conn.close()

    def vk_user_editor(self, age, gender, city, user_id):
        # 3. Функция, позволяющая изменить данные о юзере
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""UPDATE vk_user SET age = %s, gender = %s, city = %s WHERE id = %s;""",
                        (age, gender, city, user_id))
            conn.commit()
        conn.close()

    def favorites(self, vk_user_id, name, surname, profile_url, photos):
        # 4. Функция, позволяющая добавить в избранные новую запись.
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO favorites(vk_user_id, name, surname, profile_url, photos) VALUES (%s, %s, %s, %s, %s);""",
                (vk_user_id, name, surname, profile_url, photos))
            conn.commit()
        conn.close()

    def fav_user(self, vk_user_id, fav_id):
        # 5. Функция, позволяющая добавить новую запись в избранные юзера.
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO user_favorites(vk_user_id, fav_id) VALUES (%s, %s);""", (vk_user_id, fav_id))
            conn.commit()
        conn.close()

    def get_fav_users(self, vk_user_id):
        # 6. Функция, выводит список избранных людей юзера
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT name, surname, profile_url, photos FROM user_favorites uf 
                LEFT JOIN favorites f ON uf.fav_id = f.id
                WHERE vk_user_id = %s;       
            """, (vk_user_id,))
            print(cur.fetchall())

    def vk_user_removal(self, table, id):
        # 7. Функция, позволяющая удалить запись из таблицы по id
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(f"""DELETE FROM {table} WHERE id=%s;""", id)
            conn.commit()
        conn.close()
