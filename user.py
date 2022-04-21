import requests
from pprint import pprint
from work_db import check_user_search


class User(object):
    def __init__(self, token):
        self.token = token

    def user_info(self, user_id):
        url = 'https://api.vk.com/method/users.get'
        params = {
            'access_token': self.token,
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

    def users_search(self, dict, relation=6):
        if dict['sex'] == 2:
            sex = 1
        else:
            sex = 2
        url = 'https://api.vk.com/method/users.search'
        params = {
            'access_token': self.token,
            'hometown': dict['city'],
            'sex': sex,
            'status': relation,
            'birth_year': dict['age'],
            'fields': 'is_closed',
            'v': '5.131'}
        result = requests.get(url, params)
        user_search_id = None
        for item in result.json()['response']['items']:
            if item['is_closed'] == False:
                if item['id'] not in check_user_search():
                    user_search_id = item['id']
                    break
        return user_search_id

    def user_foto(self, user_id):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.token,
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
