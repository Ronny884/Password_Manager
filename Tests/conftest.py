import pytest
import os
import sqlite3 as sq

test_databases_path = f'{os.getcwd()}/Tests/test_databases'
target_db_path = os.path.join(test_databases_path, 'target_db.db')


@pytest.fixture()
def remove_new_db_before_creating():
    yield
    names = ('111', 'MyDb', 'PASSWORDS', 'NULL', 'test_db')
    for name in names:
        file_path = os.path.join(test_databases_path, f'{name}.db')
        if os.path.isfile(file_path):
            os.remove(file_path)


@pytest.fixture()
def create_target_db():
    with sq.connect(target_db_path) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS notes (
                          id INTEGER PRIMARY KEY NOT NULL,
                          name TEXT NOT NULL,
                          username TEXT,
                          password TEXT NOT NULL,
                          login TEXT,
                          passphrase TEXT,
                          phone_number TEXT,
                          url TEXT,
                          category TEXT
                          )''')
    yield
    with sq.connect(target_db_path) as con:
        cur = con.cursor()
        cur.execute('''DELETE FROM notes''')


@pytest.fixture()
def remove_incorrect_db():
    yield
    incorrect_db = os.path.join(test_databases_path, 'nonexistent_db.db')
    if os.path.isfile(incorrect_db):
        os.remove(incorrect_db)


@pytest.fixture()
def insert_true_data():
    with sq.connect(target_db_path) as con:
        cur = con.cursor()
        cur.execute('''
    INSERT INTO notes VALUES
    (1, 'Belarus', '2', '3', '4', '5', '6', '7', 'state'), 
    (2, 'Russia', 'hytuy', 'ht', '45657', 'bhjkyui', 'nbv', '7', 'state'), 
    (3, 'USA', NULL, 'nubnn', NULL, NULL, NULL, NULL, 'state'),
    (4, 'Telegram', 'Robby', 'vgbgVCVfbgH5667', 'mnbhvgbnmnbv', 'Let is go!', '+3736796535', 'www.telegram.com', 'social'),
    (5, 'VK', 'Igor', 'nhjbhgvknR&po', 'mnbhvgv', 'Ivanov', '+3736258535', 'www.vk.com', 'social'),
    (6, 'Instagram', '__ygbn_55', 'HVHbgnhbgvvVRVFVfb', '876543456', NULL, NULL, 'www.instagram.com', 'social'),
    (7, 'BritishBank', 'BB', 'dnwjbhefbndkf', 'dfgf', NULL, NULL, 'www.bb.com', NULL)
    ''')
