import requests
from pprint import pprint
from work_db import check_user_search


def init_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()


def user_info(user_id):
    TOKEN = init_token()
    url = 'https://api.vk.com/method/users.get'
    params = {
        'access_token': TOKEN,
        'user_ids': user_id,
        'fields': 'bdate, sex, city',
        'v': '5.131'}
    result = requests.get(url, params)
    user_info_dict = {}
    user_info_ = result.json()['response'][0]
    if 'sex' not in user_info_.keys():
        user_info_dict['sex'] = None
    else:
        user_info_dict['sex'] = user_info_['sex']

    if 'bdate' not in user_info_.keys():
        user_info_dict['age'] = None
    else:
        bdate = user_info_['bdate']
        if len(bdate.split('.')) < 3:
            user_info_dict['age'] = None
        else:
            user_info_dict['age'] = bdate.split('.')[2]

    if 'city' not in user_info_.keys():
        user_info_dict['city'] = None
    else:
        user_info_dict['city'] = user_info_['city']['title']

    user_info_dict['name'] = user_info_['first_name'] + ' ' + user_info_['last_name']
    return user_info_dict


def users_search(dict, relation=6):
    TOKEN = init_token()
    url = 'https://api.vk.com/method/users.search'
    params = {
        'access_token': TOKEN,
        'hometown': dict['city'],
        'sex': dict['sex'],
        'status': relation,
        'birth_year': dict['age'],
        'fields': 'is_closed',
        'v': '5.131'}
    result = requests.get(url, params)
    user_search_id = []
    for item in result.json()['response']['items']:
        if item['is_closed'] == False:
            if item['id'] not in check_user_search():
                user_search_id.append(item['id'])
                if len(user_search_id) == 3:
                    break
    return user_search_id


def user_foto(user_id):
    TOKEN = init_token()
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'access_token': TOKEN,
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': 1,
        'v': '5.131'}
    result = requests.get(url, params)

    photo_profile = {}
    for item in result.json()['response']['items']:
        comments = item['comments']['count']
        likes = item['likes']['count']
        photo = item['id']
        photo_profile[photo] = int(comments + likes)

    sorted_values = sorted(photo_profile.items(), key=lambda x: x[1])
    sorted_values.reverse()

    top_photo_profile = []
    for i in sorted_values[0:3]:
        top_photo_profile.append(i[0])
    return top_photo_profile


if __name__ == '__main__':

    print(1)
