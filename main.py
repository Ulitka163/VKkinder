from random import randrange
import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from user import User
from work_db import create_user_search, check_user, create_user_info, check_user_info, update_user_info, create_user

token = input('Token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

with open('token.txt', 'r') as file:
    TOKEN = file.read().strip()
user = User(TOKEN)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


def write_msg_attachment(user_id, attachment):
    vk.method('messages.send', {'user_id': user_id, 'attachment': attachment, 'random_id': randrange(10 ** 7), })


def complet_user_info(user_id):    # проверка на полноту информации нужной для поиска
    user_info_dict = check_user_info(user_id)
    for key, value in user_info_dict.items():
        if value == 'None':
            if key == 'sex':
                return write_msg(event.user_id, f'Введите пол пользователя(ж, м):')
            elif key == 'city':
                return write_msg(event.user_id, f'Введите город пользователя:')
            elif key == 'age':
                return write_msg(event.user_id, f'Введите год рождения пользователя:')
    return correct_answer()


def correct_answer():    # Вывод пользователя с требуемой информацией
    user_info_dict = check_user_info(user_id_)
    id_ = user.users_search(user_info_dict)
    if id_ == None:
        return write_msg(event.user_id, f'по данным параметрам пользователи закончились')
    create_user_search(user_id_, id_)
    write_msg(event.user_id, f'https://vk.com/id{id_}')
    photos = user.user_foto(id_)
    for photo in photos:
        write_msg_attachment(event.user_id, f'photo{id_}_{photo} ')


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                user_id_ = event.user_id
                write_msg(event.user_id, f"Хай, {user.user_info(user_id_)['name']}"
                                         f"\n Для поиска пользователя введите команду: 'поиск'"
                                         f"\n Для вывода следующего пользователя введите команду: 'дальше' ")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif request == "поиск":    # Поиск пользователя подходящего по параметрам
                user_id_ = event.user_id
                if len(check_user(user_id_)) == 0:
                    create_user(user_id_)
                    user_info_dict = user.user_info(user_id_)
                    create_user_info(user_id_, user_info_dict)
                    complet_user_info(user_id_)
                else:
                    correct_answer()

            elif request == "дальше":   # Поиск следующего пользователя подходящего по параметрам
                user_id_ = event.user_id
                correct_answer()

            elif re.search(r'^\d{4}$', request):     # проверка входящего сообщения: на год рождения
                user_id_ = event.user_id
                user_info_id = check_user(user_id_)[0][0]
                update_user_info(request, 'birth_year', user_info_id)
                complet_user_info(user_id_)

            elif re.search(r'^[А-я]*$', request):     # проверка входящего сообщения: на Город
                user_id_ = event.user_id
                user_info_id = check_user(user_id_)[0][0]
                update_user_info(request, 'city', user_info_id)
                complet_user_info(user_id_)

            elif re.search(r'^(м|ж)$', request):      # проверка входящего сообщения: на пол пользователя
                user_id_ = event.user_id
                user_info_id = check_user(user_id_)[0][0]
                if request == 'м':
                    update_user_info(2, 'sex', user_info_id)
                else:
                    update_user_info(1, 'sex', user_info_id)
                complet_user_info(user_id_)






