import requests
import json
from bs4 import BeautifulSoup

with open('VKAccounts.json', 'r') as f:   #Открытие файла с данными аккаунтов
    Fjson = json.loads(f.read())

if Fjson:                                 #Если все нормально открылось и данные присутствуют
    for current_account in Fjson:         #В цыкле проходим каждый аккаунт и авторизуем его на сайтах
        nick = current_account['nick']
        email = current_account['email']
        password = current_account['pass']

        print(f'Curent nick: {nick}')

        session = requests.Session()      #Открываем сессию (хз зачем, но псть будет)

        token_page = session.get('https://minecraftrating.ru/projects/excalibur-craft/')  #делаем запрос для получения страницы с токеном
        token_page_text = token_page.text           #Достаём HTML-код из ответа
        soup = BeautifulSoup(token_page_text, 'lxml')   #Скармливаем код BeautifulSoup

        token = soup.select('input[name=_token]')[0]['value'] #Достаём токен
        print(f'Token: {token}')
        url = 'excalibur-craft'          #Ссылка на проект (можно посмортеть на сайте)

        headers = {                      #Заголовки для запроса (не критически важно, можно заменить user-agent)
            'authority': 'minecraftrating.ru',
            'method': 'GET',
            'path': '/projects/excalibur-craft/',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9,fr;q=0.8',
            'cache-control': 'no-cache',
            'dnt': '1',
            'pragma': 'no-cache',
            'referer': 'https://minecraftrating.ru/',
            'sec-ch-ua': '" Not;A Brand";v="99", "Yandex";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'
        }

        #делаем пост запрос и отправляем токен, ссылку и ник, который достали из JSON файла
        vote = session.post('https://minecraftrating.ru/projects/vote/', data={'_token': token, 'url': url, 'nick': nick}, headers=headers)
        #Достаем необходимые данные (это уже страница входа в ВК, т.к. прошлая странице гедиректнула нас сюда
        vote_soup = BeautifulSoup(vote.text, 'lxml')
        ip_h = vote_soup.select('input[name=ip_h]')[0]['value']
        lg_h = vote_soup.select('input[name=lg_h]')[0]['value']
        _origin = vote_soup.select('input[name=_origin]')[0]['value']
        to = vote_soup.select('input[name=to]')[0]['value']
        expire = vote_soup.select('input[name=expire]')[0]['value']
        print(f"ip_h: {ip_h}\nlg_h: {lg_h}\n_origin: {_origin}\nto: {to}\nexpire: {expire}")

        #Словарь с данными, которые мы отправляем для авторизации (важно чтобы авторизация производилась ранее, иначе ВК попросит подтверждение на доступ к данным)
        data={
            'ip_h': ip_h,
            'lg_h': lg_h,
            '_origin': _origin,
            'to': to,
            'expire': expire,
            'email': email,
            'pass': password
            }
        headers_VK={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36'
        }
        #Отправляем запрос с данными для авторизации, если все пройдет ок, то нас редиректнит на первую страницу (см. первый гет запрос)
        VK = session.post('https://login.vk.com/?act=login&soft=1', data=data, headers=headers_VK)
        result_sous = BeautifulSoup(VK.text, 'lxml')
        promotion_alert = result_sous.select('.promotion-alert')[0].get_text()
        print(f"Response text: {promotion_alert}")

else:
    #Если файл в данными будет пустым, то выведется сообщение с ошибкой
    print("Error: the accounts file (VKAccounts.json) could not be processed")


