import os
import configparser


def cerate_db(login, name):
    return os.system(f'createdb -U {login} {name}')

def drop_db():
    return os.system(f'dropdb {name}')

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("base_settings.ini")

    db_name = config['Database']['db_name']
    user_name = config['Database']['user_name']

    cerate_db(user_name, db_name)
    # drop_db(db_name)