from PyQt6 import QtSql
import os


class DataManager:

    @staticmethod
    def create_new_db(path):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(path)
        db.open()
        try:
            query = QtSql.QSqlQuery()
            query.exec('''CREATE TABLE IF NOT EXISTS notes (
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
            query.exec()
        finally:
            db.close()

    @staticmethod
    def add_new_note_to_target_db(path, query_values):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(path)
        db.open()
        try:
            query = QtSql.QSqlQuery()
            query.prepare('''
                    INSERT INTO notes (name, username, password, login, passphrase, phone_number, url, category) 
                    VALUES (?,?,?,?,?,?,?,?)''')
            for query_value in query_values:
                query.addBindValue(query_value)
            query.exec()
        finally:
            db.close()

    @staticmethod
    def select_notes_with_or_without_category(path, category):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(path)
        db.open()

        query = QtSql.QSqlQuery()
        name_list = []
        if category is None:
            query.exec('SELECT name FROM notes')
            while query.next():
                name_list.append(query.value(0))
        else:
            query.exec('SELECT name FROM notes WHERE category = ?')
            query.bindValue(0, category)
            if query.exec():
                while query.next():
                    name_list.append(query.value(0))
        db.close()
        return name_list

    @staticmethod
    def select_all_categories(path):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(path)
            db.open()
            query = QtSql.QSqlQuery()
            category_list = []
            query.exec('SELECT category FROM notes')
            while query.next():
                category_list.append(query.value(0))
            db.close()
            return category_list
        except:
            return False

    @staticmethod
    def select_parameter_for_copy(path, note_name, parameter_for_copy):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(path)
        db.open()

        def select_password():
            password = None
            query = QtSql.QSqlQuery()
            query.exec("SELECT password FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    password = query.value(0)
            return password

        def select_login():
            login = None
            query = QtSql.QSqlQuery()
            query.exec("SELECT login FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    login = query.value(0)
            return login

        def select_username():
            username = None
            query = QtSql.QSqlQuery()
            query.exec("SELECT username FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    username = query.value(0)
            return username

        def select_passphrase():
            passphrase = None
            query = QtSql.QSqlQuery()
            query.exec("SELECT passphrase FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    passphrase = query.value(0)
            return passphrase

        def select_phone_number():
            phone_number = None
            query = QtSql.QSqlQuery()
            query.exec("SELECT phone_number FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    phone_number = query.value(0)
            return phone_number

        def select_url():
            url = None
            query = QtSql.QSqlQuery()
            query.exec("SELECT url FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    url = query.value(0)
            return url

        def select_category():
            category = None
            query = QtSql.QSqlQuery()
            query.exec("SELECT category FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    category = query.value(0)
            return category

        def get_id():
            note_id = None
            query = QtSql.QSqlQuery()
            query.exec("SELECT id FROM notes WHERE name = ?")
            query.bindValue(0, note_name)
            if query.exec():
                while query.next():
                    note_id = query.value(0)
            return note_id

        functions_for_parameters = {
            'password': select_password,
            'login': select_login,
            'username': select_username,
            'passphrase': select_passphrase,
            'phone_number': select_phone_number,
            'category': select_category,
            'url': select_url,
            'id': get_id}

        return functions_for_parameters[parameter_for_copy]()

    @staticmethod
    def delete_note(path, note_name):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(path)
        db.open()
        query = QtSql.QSqlQuery()
        query.exec('DELETE FROM notes WHERE name = ?')
        query.bindValue(0, note_name)
        query.exec()
        db.close()

    @staticmethod
    def get_name_by_id(path, id):
        name = None
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(path)
        db.open()
        query = QtSql.QSqlQuery()
        query.exec('SELECT name FROM notes WHERE id = ?')
        query.bindValue(0, id)
        if query.exec():
            while query.next():
                name = query.value(0)
        db.close()
        return name

    @staticmethod
    def update_note(path, query_values):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(path)
        db.open()
        query = QtSql.QSqlQuery()
        query.prepare('''
        UPDATE notes SET name=?, username=?, password=?, login=?, passphrase=?, phone_number=?, url=?, category=? 
        WHERE id=?''')
        for query_value in query_values:
            query.addBindValue(query_value)
        query.exec()
        db.close()

    @staticmethod
    def repition_chek(path, name):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(path)
            db.open()
            query = QtSql.QSqlQuery()
            name_list = []
            query.exec('SELECT name FROM notes')
            while query.next():
                name_list.append(query.value(0))
            db.close()
            if name not in name_list:
                return True
            else:
                return False
        except:
            return None
