import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://vkkinder:qwerty@localhost:5432/vkkinder_db')
connection = engine.connect()

def check_user(vk_id):
    result = connection.execute(f'''SELECT id FROM user_vk
     WHERE vk_id IN ('{vk_id}') ;
''').fetchall()
    return result


def check_user_search():
    result = connection.execute(f'''SELECT vk_id_search FROM user_search
    ;
''').fetchall()
    user_search_list = []
    for i in result:
        user_search_list.append(int(i[0]))
    return user_search_list


def create_user(vk_id):
    connection.execute(f'''INSERT INTO user_vk(vk_id)
    VALUES({vk_id});
    ''')


def create_user_info(id, name, sex, city, birth_year):
    connection.execute(f'''INSERT INTO user_info
    VALUES({id}, {name}, {sex}, {city}, {birth_year});
    ''')


def create_user_search(user_id, user_search_id):
    connection.execute(f'''INSERT INTO user_search
    VALUES({user_id}, {user_search_id});
    ''')

if __name__ == '__main__':
    # print(check_user(314747176))
    print(check_user_search())