import requests
import os
from datetime import datetime, timedelta


# Задание 1
def most_intelligent_hero(compare_hero_list):
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    resp = requests.get(url)
    all_heroes_list = resp.json()
    hero_intelligence_dict = {}
    for compare_hero in compare_hero_list:
        for hero in all_heroes_list:
            if hero['name'] == compare_hero:
                hero_intelligence_dict[compare_hero] = hero['powerstats']['intelligence']
                break
    return max(hero_intelligence_dict, key=hero_intelligence_dict.get)


# Задание 2
class YaUploader:
    def __init__(self, token):
        self.token = token

    def create_folder(self, folder):
        create_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': self.token}
        params = {'path': folder, 'overwrite': 'true'}
        resp = requests.put(create_url, headers=headers, params=params)
        if resp.status_code == 201:
            print(f'Папка {folder} успешно создана на яндекс.диске.')
        elif resp.status_code == 409:
            print(f'Папка {folder} уже существует на яндекс.диске.')
        else:
            print('Возможно указан не верный OAuth токен')
        return

    def upload(self, ya_disk_file_path, filename):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Accept': 'application/json', 'Authorization': self.token}
        path = ya_disk_file_path + '/' + filename
        params = {'path': path, 'overwrite': 'true'}
        href = requests.get(upload_url, headers=headers, params=params).json().get('href')
        FILE_NAME = filename
        full_path_f = os.path.join(FILE_NAME)
        resp = requests.put(href, data=open(full_path_f, 'rb'))
        resp.raise_for_status()
        if resp.status_code == 201:
            print(f'Файл {filename} успешно записан в папку {ya_disk_file_path} на яндекс.диске.')
        return


# Задание 3. Все запросы с тегом Python за последние 2 дня со Stackoverflow.

# Возвращает текущую дату и дату n-дней назад.
def two_date(days):
    to_date = datetime.today().date()
    from_date = to_date - timedelta(days=days)
    date_interval = [from_date, to_date]
    return date_interval


# Возвращает список вопросов за указанный интервал по указанному тегу
def get_questions(date_interval, tag):
    url = 'https://api.stackexchange.com/2.3/questions'
    params = {'fromdate': date_interval[0], 'todate': date_interval[1], 'tagged': tag, 'site': 'stackoverflow'}
    href = requests.get(url, params=params)
    list_dict_questions = href.json().get('items')
    result_list = []
    for dict_questions in list_dict_questions:
        result_list.append(dict_questions.get('title'))
    return result_list


if __name__ == '__main__':
    # Задание 1
    compare_hero_list_ = ['Hulk', 'Captain America', 'Thanos']
    print(f'Самый умный из {len(compare_hero_list_)} супергероев ', end='')
    count = 0
    for hero_ in compare_hero_list_:
        count += 1
        if count != len(compare_hero_list_):
            print(hero_, end=', ')
        else:
            print(hero_, end=': ')
    print(f'{most_intelligent_hero(compare_hero_list_)}.')
    print('___________________________________________________________')

    # # Задание 2. (Ввести свой токен и раскомментировать блок)

    # # Получить путь к загружаемому файлу и токен от пользователя
    # filename_ = 'test_upload.txt'
    # token_ = 'your_token'  # Скопировать сюда свой OAuth токен.
    # ya_disk_file_path_ = 'Python'  # Папка куда загружаем файл на яндекс.диск
    # ya_uploader = YaUploader(token_)
    # ya_uploader.create_folder(ya_disk_file_path_)  # Создаём папку на яндекс.диске
    # ya_uploader.upload(ya_disk_file_path_, filename_)  # Загружаем файл на яндекс.диск в указанную папку
    # print('___________________________________________________________')

    # Задание 3
    date_list = two_date(2)  # Аргумент: за какое кол-во дней осуществлять выборку
    list_questions = get_questions(date_list, 'Python') 
    for _ in list_questions:
        print(_)

