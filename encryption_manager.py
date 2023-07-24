from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from file_manager import FileManager


class EncryptionManager(FileManager):

    def encrypt_file(self, db_name_without_extension, password):
        """
        Функция шифрует БД: создаёт соль и сохраняет её в отдельный файл, что также шифруется под ключ из
        указанного мастер-пароля (сохраняется в переменную) и соль, что прописана в коде. Вызывается функция, если
        пользователь после создания БД в окне 5 вернётся в главное меню, если из окна 9 (10) при работе сданной БД
        решит вернуться в окно 3 или окно 1, а также, если закроет программу, нажав на крестик
        """
        try:
            # формируем ключ для файла с солью
            salt_for_salt = b'\xfbJ\x05\x14d\x0b\xb3\xd5o\x9b<\xbb\x84l\xb0\xb1\x8b\xe9\x10\x0c\xa8\xde\x1c3\x91\xac\xcaK\xe9\xc9\xafa'
            key_for_salt = PBKDF2(password, salt_for_salt, dkLen=32)

            salt = get_random_bytes(32)  # формируем соль для файла БД
            key = PBKDF2(password, salt, dkLen=32)  # формируем ключ для файла БД

            # self.create_a_folder_if_it_does_not_exist()

            # сохраняем соль в файл
            self.save_salt_to_special_file(db_name_without_extension, salt)

            # зашифровываем этот файл под фиксированную соль salt_for_salt и пароль
            iv = get_random_bytes(16)
            cipher = AES.new(key_for_salt, AES.MODE_CBC, iv)
            file_name_with_extension = f'{db_name_without_extension}.bin'
            plaintext = self.get_data_from_file('Alpha', file_name_with_extension)
            ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
            self.set_ciphertext_to_file('Alpha', file_name_with_extension, iv, ciphertext)

            # зашифровываем непосредственно сам файл с БД, что к тому моменту уже сохранена
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            file_name_with_extension = f'{db_name_without_extension}.db'
            plaintext = self.get_data_from_file('Database', file_name_with_extension)
            ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
            self.set_ciphertext_to_file('Database', file_name_with_extension, iv, ciphertext)
        except Exception as e:
            return (str(e))

    def decrypt_file(self, db_name_without_extension, password):
        """
        Функция для дешифровки сначала файла с солью, затем файла БД в случае верного мастер-пароля. Вызывается после
        ввода мастер-пароля в окне 4 при начале работы с ранее сохранённой базой.
        """
        try:
            # формируем ключ для файла с солью
            salt_for_salt = b'\xfbJ\x05\x14d\x0b\xb3\xd5o\x9b<\xbb\x84l\xb0\xb1\x8b\xe9\x10\x0c\xa8\xde\x1c3\x91\xac\xcaK\xe9\xc9\xafa'
            key_for_salt = PBKDF2(password, salt_for_salt, dkLen=32)

            # расшифровываем файл с солью, не изменяя его и берём оттуда соль
            file_name_with_extension = f'{db_name_without_extension}.bin'
            data = self.get_data_from_file('Alpha', file_name_with_extension)
            iv = data[:16]
            ciphertext = data[16:]
            cipher = AES.new(key_for_salt, AES.MODE_CBC, iv)
            plaintext_salt = unpad(cipher.decrypt(ciphertext), AES.block_size)

            # формируем ключ для файла БД
            key = PBKDF2(password, plaintext_salt, dkLen=32)

            # расшифровываем файл с БД
            file_name_with_extension = f'{db_name_without_extension}.db'
            data = self.get_data_from_file('Database', file_name_with_extension)
            iv = data[:16]
            ciphertext = data[16:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            self.set_plaintext_to_file('Database', file_name_with_extension, plaintext)
            return True
        except:
            return False

    def encryption_before_closing_the_program(self, unsafe_windows):
        """
        Функция вызывает метод шифрования при выходе из программы через нажатие на крестик, а так же метод работы с
        файлом блокировки второго экземпляра приложения
        """
        for window in unsafe_windows:
            if window.tuple_with_need_name_and_password[0] is True:
                print(window.tuple_with_need_name_and_password[1], window.tuple_with_need_name_and_password[2])
                self.encrypt_file(window.tuple_with_need_name_and_password[1], window.tuple_with_need_name_and_password[2])
        self.remove_lock_file()



