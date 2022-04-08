import requests
from pprint import pprint
from work_db import create_user


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
    sex = result.json()['response'][0]['sex']
    bdate = result.json()['response'][0]['bdate']
    age = bdate.split('.')[2]
    city = result.json()['response'][0]['city']['id']
    return [sex, city, age]


def users_search(sex, hometown, birth_year, relation=6):
    TOKEN = init_token()
    url = 'https://api.vk.com/method/users.search'
    params = {
        'access_token': TOKEN,
        'city': hometown,
        'sex': sex,
        'status': relation,
        'birth_year': birth_year,
        'count': 3,
        'v': '5.131'}
    result = requests.get(url, params)
    user_search_id = []
    for item in result.json()['response']['items']:
        user_search_id.append(item['id'])
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

    print(user_info(1373131))
