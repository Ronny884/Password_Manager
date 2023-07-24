import os
from PyQt6.QtWidgets import QMessageBox


class FileManager:

    @staticmethod
    def check_lock_file():
        LOCK_FILE_PATH = f'{os.getcwd()}/file.lock'
        if os.path.exists(LOCK_FILE_PATH):
            QMessageBox.critical(None, "Error", "Another instance of the application is already running.")
            return False
        else:
            try:
                with open(LOCK_FILE_PATH, "w"):
                    pass
                return True
            except IOError:
                QMessageBox.critical(None, "Error", "Failed to create lock file.")
                return False

    @staticmethod
    def remove_lock_file():
        LOCK_FILE_PATH = f'{os.getcwd()}/file.lock'
        if os.path.exists(LOCK_FILE_PATH):
            os.remove(LOCK_FILE_PATH)

    @staticmethod
    def create_a_folder_if_it_does_not_exist():
        if not os.path.exists(f'{os.getcwd()}/Database'):
            os.mkdir(f'{os.getcwd()}/Database')
        if not os.path.exists(f'{os.getcwd()}/Alpha'):
            os.mkdir(f'{os.getcwd()}/Alpha')

    @staticmethod
    def save_salt_to_special_file(db_name_without_extension, salt):
        with open(f'{os.getcwd()}/Alpha/{db_name_without_extension}.bin', 'wb') as file:
            file.write(salt)

    @staticmethod
    def get_data_from_file(folder, file_name_with_extension):
        with open(f'{os.getcwd()}/{folder}/{file_name_with_extension}', 'rb') as file:
            data = file.read()
        return data

    @staticmethod
    def set_ciphertext_to_file(folder, file_name_with_extension, iv, ciphertext):
        with open(f'{os.getcwd()}/{folder}/{file_name_with_extension}', 'wb') as file:
            file.write(iv + ciphertext)

    @staticmethod
    def set_plaintext_to_file(folder, file_name_with_extension, plaintext):
        with open(f'{os.getcwd()}/{folder}/{file_name_with_extension}', 'wb') as file:
            file.write(plaintext)

    @staticmethod
    def check_for_db_file():
        for file_name in os.listdir(f'{os.getcwd()}/Database'):
            if file_name.endswith('.db'):
                return True
            else:
                return False

    @staticmethod
    def checking_for_folder_existence(folder):
        if os.path.exists(f'{os.getcwd()}/{folder}'):
            return True
        else:
            return False

    @staticmethod
    def checking_for_file_existence(folder, filename):
        path = f'{os.getcwd()}/{folder}/{filename}'
        if os.path.isfile(path):
            return True
        else:
            return False

    @staticmethod
    def get_listdir(folder):
        return os.listdir(f'{os.getcwd()}/{folder}')