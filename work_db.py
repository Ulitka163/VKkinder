import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://vkkinder:qwerty@localhost:5432/vkkinder_db')
connection = engine.connect()


def check_user(vk_id):
    result = connection.execute(f'''SELECT id FROM user_vk
     WHERE vk_id = '{vk_id}';
''').fetchall()
    return result


def check_user_info(vk_id):
    user_id = check_user(vk_id)[0][0]
    result = connection.execute(f'''SELECT sex, city, birth_year FROM user_info
    WHERE id = {user_id};
''').fetchall()
    check_user_info_dict = {'sex': result[0][0], 'city': result[0][1], 'age': result[0][2]}
    return check_user_info_dict


def check_user_search():
    result = connection.execute(f'''SELECT vk_id_search FROM user_search;
''').fetchall()
    user_search_list = []
    for i in result:
        user_search_list.append(int(i[0]))
    return user_search_list


def create_user(vk_id):
    connection.execute(f'''INSERT INTO user_vk(vk_id)
    VALUES('{vk_id}');
    ''')


def create_user_info(vk_id, dict):
    user_id = check_user(vk_id)[0][0]
    connection.execute(f'''INSERT INTO user_info
    VALUES({user_id}, '{dict['name']}', {dict['sex']}, '{dict['city']}', {dict['age']});
    ''')


def create_user_search(vk_id, user_search_id):
    user_id = check_user(vk_id)[0][0]
    connection.execute(f'''INSERT INTO user_search
    VALUES('{user_id}', {user_search_id});
    ''')


def update_user_info(value, column, user_id):
    connection.execute(f'''UPDATE user_info
    SET {column} = '{value}'
    WHERE id = {user_id};
''')


if __name__ == '__main__':
    print(check_user(314747176))
    # print(check_user_search())