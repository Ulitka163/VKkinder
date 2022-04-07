from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from user import user_info, users_search, user_foto

token = input('Token: ')

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                user_info_ = user_info(event.user_id)
                id = users_search(user_info_[0], user_info_[1], user_info_[2])
                photo = user_foto(id)

                write_msg(event.user_id, photo[0])




