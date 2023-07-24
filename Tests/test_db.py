import os
import sqlite3 as sq
import pytest
import pytest_randomly
from data_manager import DataManager
from file_manager import FileManager

db = DataManager()
f = FileManager()
test_databases_path = f'{os.getcwd()}/Tests/test_databases'
target_db_path = os.path.join(test_databases_path, 'target_db.db')


def get_note(path, query_values=None, name=None):
    with sq.connect(path) as con:
        cur = con.cursor()
        if name is None:
            cur.execute(f'''SELECT * FROM notes WHERE name = "{query_values[0]}"''')
        else:
            cur.execute(f'''SELECT * FROM notes WHERE name = "{name}"''')
        res = cur.fetchall()
    return res


def get_count(path):
    with sq.connect(path) as con:
        cur = con.cursor()
        cur.execute('''SELECT count() FROM notes''')
        res = cur.fetchall()
        return res


@pytest.mark.parametrize('path', [os.path.join(test_databases_path, '111.db'),
                                  os.path.join(test_databases_path, 'MyDb.db'),
                                  os.path.join(test_databases_path, 'PASSWORDS.db'),
                                  os.path.join(test_databases_path, 'NULL.db'),
                                  os.path.join(test_databases_path, 'test_db.db')])
def test_create_new_db(remove_new_db_before_creating, path):
    db.create_new_db(path)
    assert os.path.isfile(path)


@pytest.mark.parametrize('path, query_values', [
    (target_db_path, ('Belarus', '2', '3', '4', '5', '6', '7', 'state')),
    (target_db_path, ('Russia', 'hytuy', 'ht', '45657', 'bhjkyui', 'nbv', '7', 'state')),
    (target_db_path, ('USA', None, 'nubnn', None, None, None, None, None)),
    (target_db_path, (
    'Telegram', 'Robby', 'vgbgVCVfbgH5667', 'mnbhvgbnmnbv', 'Let is go!', '+3736796535', 'www.telegram.com', 'social')),
    (target_db_path, ('None', 'Igor', 'nhjbhgvknR&(po', 'mnbhvgv', 'Ivanov', '+3736258535', 'www.vk.com', 'social')),
    (target_db_path,
     ('Instagram', '__ygbn_55', 'HVHbgnhbgvvVRVFVfb', '876543456', None, None, 'www.instagram.com', None))
])
def test_add_new_note_to_target_db_successful(create_target_db, path, query_values):
    db.add_new_note_to_target_db(path, query_values)
    assert get_note(path, query_values)[0][1:] == query_values


@pytest.mark.parametrize('path, query_values', [
    (target_db_path, (None, None, 'nubnn', 'vrsfd', 'rsdg', 'dv', 'gh', 'tgd')),
    (target_db_path, ('Note', 'dccd', None, '4', '5', '6', '7', '9')),
    (os.path.join(test_databases_path, 'nonexistent_db.db'), ('Note', 'dccd', 'cfdw', '4', '5', '6', '7', '9')),
    (target_db_path, (None, 'dccd', None, '4', '5', '6', '7', '9')),
    (target_db_path, ('333', 'dccd', 'dfd', '4', '5', '6'))
])
def test_add_new_note_to_target_db_incorrect(create_target_db, remove_incorrect_db, path, query_values):
    with pytest.raises(Exception):
        db.add_new_note_to_target_db(path, query_values)
        note = get_note(path, query_values)[0][1:]


@pytest.mark.parametrize('path, category', [
    (target_db_path, None),
    (target_db_path, 'state'),
    (target_db_path, 'social')
])
def test_select_notes_with_or_without_category(create_target_db, insert_true_data, path, category):
    true_data = {None: ['Belarus', 'Russia', 'USA', 'Telegram', 'VK', 'Instagram', 'BritishBank'],
                 'state': ['Belarus', 'Russia', 'USA'],
                 'social': ['Telegram', 'VK', 'Instagram']}
    assert db.select_notes_with_or_without_category(path, category) == true_data[category]


@pytest.mark.parametrize('path', [target_db_path])
def test_select_all_categories(create_target_db, insert_true_data, path):
    true_data = ['state', 'social']
    res_data = db.select_all_categories(path)
    res_data.remove('')
    assert sorted(list(set(res_data))) == sorted(true_data)


@pytest.mark.parametrize('path, note_name, parameter_for_copy', [
    (target_db_path, 'Telegram', 'password'),
    (target_db_path, 'VK', 'url'),
    (target_db_path, 'Instagram', 'username'),
    (target_db_path, 'Belarus', 'category'),
    (target_db_path, 'Russia', 'id'),
    (target_db_path, 'USA', 'login')
])
def test_select_parameter_for_copy(create_target_db, insert_true_data, path, note_name, parameter_for_copy):
    true_res = {'Telegram': 'vgbgVCVfbgH5667',
                'VK': 'www.vk.com',
                'Instagram': '__ygbn_55',
                'Belarus': 'state',
                'Russia': 2,
                'USA': ''}
    assert db.select_parameter_for_copy(path, note_name, parameter_for_copy) == true_res[note_name]


@pytest.mark.parametrize('path, note_name', [
    (target_db_path, 'Telegram'),
    (target_db_path, 'VK'),
    (target_db_path, 'Instagram'),
    (target_db_path, 'Belarus'),
    (target_db_path, 'Russia'),
    (target_db_path, 'USA')
])
def test_delete_note(create_target_db, insert_true_data, path, note_name):
    db.delete_note(path, note_name)
    assert get_note(path, name=note_name) == []
    assert get_count(path) == [(6,)]


@pytest.mark.parametrize('path, incorrect_note_name', [
    (target_db_path, 'Telegramm'),
    (target_db_path, 'VKK'),
    (target_db_path, 'IInstagram'),
    (target_db_path, 'bnhm'),
    (target_db_path, 'u'),
    (target_db_path, '2')
])
def test_delete_note_incorrect(create_target_db, insert_true_data, path, incorrect_note_name):
    db.delete_note(path, incorrect_note_name)
    assert get_count(path) == [(7,)]


@pytest.mark.parametrize('path, id', [
    (target_db_path, 1),
    (target_db_path, 7),
    (target_db_path, 2),
    (target_db_path, 4)
])
def test_get_name_by_id(create_target_db, insert_true_data, path, id):
    true_data = {1: 'Belarus',
                 7: 'BritishBank',
                 2: 'Russia',
                 4: 'Telegram'}
    assert db.get_name_by_id(path, id) == true_data[id]


@pytest.mark.parametrize('path, query_values', [
    (target_db_path, ('Belarus_new', '22', '33', '44', '55', '66', '77', 'state', '1')),
    (target_db_path, ('Russia_new', 'hytuy', 'ht', '45657', 'bhjkyui', 'nbv', '7', 'state', '2')),
    (target_db_path, ('USA_new', None, 'rnybfgvnhcf', None, None, None, None, None, '3')),
    (target_db_path, (
    'Telegram_new', 'Robby', 'vgbgVCVfbgH5667', 'mnbhvgbnmnbv', 'Let is go!', '+3736796535',
    'www.telegram.com', 'social', '4'))
])
def test_update_note(create_target_db, insert_true_data, path, query_values):
    db.update_note(path, query_values)
    assert get_note(path, query_values)[0][1:] == query_values[:8]


@pytest.mark.parametrize('path, name', [
    (target_db_path, 'Belarus'),
    (target_db_path, 'BritishBank'),
    (target_db_path, 'Mars'),
    (target_db_path, '4')
])
def test_repition_check(create_target_db, insert_true_data, path, name):
    true_res = {'Belarus': False,
                'BritishBank': False,
                'Mars': True,
                '4': True}
    assert db.repition_chek(path, name) == true_res[name]