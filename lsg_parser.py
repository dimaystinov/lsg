import re
import os.path
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse
import json


class lsg:
    host = 'https://lsg.ru'
    url = 'https://lsg.ru/api/crowd_data'
    lastkey = ""


    def __init__(self):
        lastkey_file = "lastkey.txt"
        self.lastkey_file = lastkey_file

        if (os.path.exists(lastkey_file)):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            f = open(lastkey_file, 'w')
            self.lastkey = self.get_lastkey()
            f.write(self.lastkey)
            f.close()

    def all_posts(self):
        r = requests.get(self.url)
        content = (r.content.decode())
        try:
            decoded = json.loads(content)
        except:
            return "Error 123. Format Error"

        return decoded

    def post(self, id):
        posts = self.all_posts()
        for post in posts:
            if post["id"] == id:
                return post
        return "None"




    def all_id(self):
        all_id_list = []
        for post in self.all_posts():
            all_id_list.append(post["id"])
        return all_id_list

    def post_info(self, url):
        link = self.host + url
        r = requests.get(link)
        html = BS(r.content, 'html.parser')

        # parse poster image url
        poster = re.match(r'background-image:\s*url\((.+?)\)', html.select('.image-game-logo > .image')[0]['style'])

        # remove some stuff
        remels = html.select('.article.article-show > *')
        for remel in remels:
            remel.extract()

        # form data
        info = {
            "id": self.parse_href(url),
            "title": html.select('.article-title > a')[0].text,
            "link": link,
            "image": poster.group(1),
            "score": self.identify_score(html.select('.game-lsg-score > .score')[0]['class'][1]),
            "excerpt": html.select('.article.article-show')[0].text[0:200] + '...'
        };

        return info

    def download_image(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def identify_score(self, score):
        if (score == 'score-1'):
            return "Мусор 👎"
        elif (score == 'score-2'):
            return "Проходняк ✋"
        elif (score == 'score-3'):
            return "Похвально 👍"
        elif (score == 'score-4'):
            return "Изумительно 👌"

    def last_id(self):

        with open(self.lastkey_file, "r+") as f:
            ids = [int(i) for i in f.read().splitlines()]

        return ids

    def update_lastkey(self):
        with open(self.lastkey_file, "w+") as f:
            try:
                for i in self.all_id():
                    f.writelines(str(i) + '\n')
            except Exception:
                print(Exception)


    def new_id(self):
        last_id = set(self.last_id())
        all_id = set(self.all_id())

        new_id = all_id - last_id

        old_id = last_id - all_id
        # print(last_id, all_id, old_id, new_id)
        if len(new_id) == 0:
            return False
        else:
            return new_id






# print(sg.new_post())

'''for post in decoded:
            print(post["id"], post["image_link"], post["name"], post["sum_now"], post["start_date"],
                  post["live_status"], post["zoom_text"])
            get_crowd_reward = post["get_crowd_reward"]
            for variant in get_crowd_reward:
                print(variant)
            s = str(post["id"]) + post["name"] + str(post["sum_now"]) + str(post["start_date"]) + post["live_status"] + str(post["zoom_text"])
            return ()'''