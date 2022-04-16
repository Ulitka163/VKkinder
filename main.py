from random import randrange
import re
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from user import user_info, users_search, user_foto
from work_db import create_user_search, check_user, create_user_info, check_user_info, update_user_info, create_user

token = input('Token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


def write_msg_attachment(user_id, attachment):
    vk.method('messages.send', {'user_id': user_id, 'attachment': attachment, 'random_id': randrange(10 ** 7), })


def complet_user_info(user_id):    # проверка на полноту информации нужной для поиска
    user_info_dict = check_user_info(user_id)
    for key, value in user_info_dict.items():
        if value == None:
            if key == 'sex':
                write_msg(event.user_id, f'Введите пол пользователя(ж, м):')
                break
            elif key == 'city':
                write_msg(event.user_id, f'Введите город пользователя:')
                break
            elif key == 'age':
                write_msg(event.user_id, f'Введите год рождения пользователя:')
                break
    return True


def correct_answer():
    user_info_dict = check_user_info(user_id)
    ids = users_search(user_info_dict)
    for id_ in ids:
        create_user_search(user_id, id_)
        write_msg(event.user_id, f'https://vk.com/id{id_}')
        photos = user_foto(id_)
        for photo in photos:
            write_msg_attachment(event.user_id, f'photo{id_}_{photo} ')


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text
            user_id = ''

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}\n Введите ID пользователя для кого мы будем искать пару (id....)")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            elif re.search(r'^id\d*$', request):    # проверка входящего сообщения: на ID пользователя
                user_id = request
                if len(check_user(user_id)) == 0:
                    create_user(user_id)
                    user_info_dict = user_info(user_id)
                    create_user_info(user_id, user_info_dict)
                    if complet_user_info(user_id):
                        correct_answer()
                else:
                    correct_answer()

            elif 1922 < int(re.search(r'^\d{4}$', request).group()) < 2022:     # проверка входящего сообщения: на год рождения
                update_user_info(request, 'birth_year', user_id)
                if complet_user_info(user_id):
                    correct_answer()

            elif re.search(r'^[А-я]$', request):     # проверка входящего сообщения: на Город
                update_user_info(request, 'city', user_id)
                if complet_user_info(user_id):
                    correct_answer()

            elif re.search(r'^(м|ж)$', request):      # проверка входящего сообщения: на пол пользователя
                if request == 'м':
                    update_user_info(2, 'sex', user_id)
                else:
                    update_user_info(1, 'sex', user_id)
                if complet_user_info(user_id):
                    correct_answer()






