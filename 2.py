import vk_api
login=input('a')
password=input('d')
vk = vk_api.VkApi(login, password)

vk.auth()
code = vk.server_auth()
a = vk.code_auth(code, 'https://oauth.vk.com/blank.html')
print(a)