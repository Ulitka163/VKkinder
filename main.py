from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from user import user_info, users_search, user_foto

token = input('Token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


def write_msg_attachment(user_id, attachment):
    vk.method('messages.send', {'user_id': user_id, 'attachment': attachment, 'random_id': randrange(10 ** 7), })


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}\n Введите ID пользователя для кого мы будем искать пару")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                user_info_ = user_info(int(event.text))

                ids = users_search(user_info_[0], user_info_[1], user_info_[2])
                for id_ in ids:
                    write_msg(event.user_id, f'https://vk.com/id{id_}')
                    photos = user_foto(id_)
                    for photo in photos:
                        write_msg_attachment(event.user_id, f'photo{id_}_{photo} ')





