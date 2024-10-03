from pprint import pprint
import os
from tqdm import tqdm
import requests
from settings import token_cfg


class VK_API:
    url = 'https://api.vk.com/method/'
    def __init__(self, access_token, user_id, vk_version='5.131'):
        self.access_token = access_token
        self.id = user_id
        self.vk_version = vk_version
        self.params = {'access_token': self.access_token, 'v': self.vk_version}

    def save_photo(self):
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1, 'count': 5}
        response = requests.get(f'{self.url}photos.get', params={**self.params, **params}).json()
        for photo in response['response']['items']:
            file_name = photo['likes']['count']
            photo_url = photo['orig_photo']['url']
            photo_response = requests.get(photo_url)
            try:
                with open(f'Image/{file_name}.jpg', 'wb') as f:
                    f.write(photo_response.content)
            except Exception as e:
                print(f"Ошибка при загрузке фото: {photo_url}, ошибка: {e}")
            else:
                print('Фотографии успешно сохранены!')




class YD_API:

    def __init__(self, access_token):
        self.headers = {'Authorization': f'OAuth {access_token}'}
        self.params = {'path': 'Photos'}

    def create_folder(self):
        YD_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        response = requests.put(YD_url, headers=self.headers, params=self.params)


    def uploading_photos(self):

        directory = 'Image'
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Директория {directory} не найдена")
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.jpg')]


        try:
            for filename in tqdm(files):
                file_path = os.path.join(directory, filename)
                response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                        params={'path': f'Photos/{filename}'},
                                        headers=self.headers).json()
                url_upload = response['href']
                with open(file_path, 'rb') as file:
                    requests.put(url_upload, files={'file': file})
        except Exception as e:
            print(e)

        else:
            print('Фотографии успешно загружены на Яндекс.Диск!')




vk_id = VK_API(token_cfg.vktoken, 260829155)
yd_id = YD_API(token_cfg.ydtoken)




