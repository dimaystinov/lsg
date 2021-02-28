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
        except Exception:
            print(Exception)
            return "Error 123. Format Error"

        return decoded

    def post(self, id):
        posts = self.all_posts()
        for post in posts:
            if post["id"] == id:
                header = [str(post["name"]), "Собрано: " + str(post["sum_now"]) + "Евро",
                          "Дата стрима: " + str(post["start_date"])]
                photo = post["image_link"]
                variants = []
                for variant in post["get_crowd_reward"]:
                    print(variant)
                    text = variant["description"]
                    soup = BS(text, features="html.parser")

                    variants.append(str(variant["name"]) + " " + soup.get_text())
                    print(soup.get_text())
                variants_btn = "1"
                variants_str = "\n\n".join(variants)
                header_str = "\n".join(header)
                head = header_str + "\n" + photo + "\n"
                return {"head": head, "variants": variants_str, "variants_btn": variants_btn}
        return "None"

    def all_id(self):
        all_id_list = []
        for post in self.all_posts():
            all_id_list.append(post["id"])
        return all_id_list

    def post_info(self, url):

        return 1

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

d = [{"id": 38, "image_link": "https:\/\/lsg.ru\/storage\/crowd\/TuLKQG4x0UHUtGbzFTFg0nA8PBpa5pGWIkZcZK0a.jpeg",
      "name": "Киберсексуальность дистанционного мира", "sum_now": 56, "start_date": "2020-03-24", "live_status": 0,
      "zoom_text": "Комната еще не активна", "get_crowd_reward": [
        {"id": 79, "lot_id": 38, "min_price": 2, "max_price": 19, "name": "Вариант №1",
         "description": "<p><strong>Позволяет: <\/strong><\/p>\r\n<p>- участвовать в трансляции;&nbsp;<\/p>\r\n<p>- получить записи стрима;&nbsp;<\/p>\r\n<p>&nbsp; &nbsp;<\/p>\r\n<p><em>*Внимание! Если Вы выбираете этот вариант и донатите свыше 20 евро, то система на вариант №2 доната автоматически не переводит<\/em><\/p>",
         "get_crowd_user_count": 22}, {"id": 80, "lot_id": 38, "min_price": 20, "max_price": 50, "name": "Вариант №2",
                                       "description": "<p><strong>Позволяет: <\/strong><\/p>\r\n<p>- участвовать в трансляции;&nbsp;<\/p>\r\n<p>- получить записи стрима;&nbsp;&nbsp;<\/p>\r\n<p>- задавать ведущим вопросы в чате;<\/p>\r\n<p>- получить транскрибацию вебинара. &nbsp; &nbsp;<\/p>\r\n<p>&nbsp;<\/p>\r\n<p><em>*Внимание! Транскрибация вебинара высылается в течение 7 дней после окончания мероприятия.<\/em><\/p>",
                                       "get_crowd_user_count": 0},
        {"id": 81, "lot_id": 38, "min_price": 50, "max_price": 100, "name": "Вариант №3",
         "description": "<p><strong>Позволяет: <\/strong><\/p>\r\n<p>- участвовать в трансляции;&nbsp;<\/p>\r\n<p>- получить записи стрима;&nbsp;<\/p>\r\n<p>- задавать ведущим вопросы в чате;<\/p>\r\n<p>- получить транскрибацию вебинара;<\/p>\r\n<p>- получить колекцию фото КиберДивы. &nbsp; &nbsp;<\/p>\r\n<p>&nbsp;<\/p>\r\n<p><em>*Внимание! Транскрибация вебинара высылается в течение 7 дней после окончания мероприятия.<\/em><\/p>",
         "get_crowd_user_count": 0}, {"id": 82, "lot_id": 38, "min_price": 100, "max_price": 300, "name": "Вариант №4",
                                      "description": "<p><strong>Позволяет: <\/strong><\/p>\r\n<p>- участвовать в трансляции;&nbsp;<\/p>\r\n<p>- получить записи стрима;&nbsp;<\/p>\r\n<p>- задавать ведущим вопросы в чате;<\/p>\r\n<p>- получить транскрибацию вебинара;<\/p>\r\n<p>- получить колекцию фото КиберДивы;<\/p>\r\n<p>- возможность задать КиберДиве вопрос индивидуально после стрима (дистанционно - 20 минут времени). &nbsp; &nbsp;<\/p>\r\n<p>&nbsp;<\/p>\r\n<p><em>*Внимание! Транскрибация вебинара высылается в течение 7 дней после окончания мероприятия.<\/em><\/p>",
                                      "get_crowd_user_count": 0},
        {"id": 83, "lot_id": 38, "min_price": 300, "max_price": 1000, "name": "Вариант №5",
         "description": "<p><strong>Позволяет:<\/strong><\/p>\r\n<p>- участвовать в трансляции;&nbsp;<\/p>\r\n<p>- получить записи стрима;&nbsp;<\/p>\r\n<p>- задавать ведущим вопросы в чате;<\/p>\r\n<p>- получить транскрибацию вебинара;<\/p>\r\n<p>- получить колекцию фото КиберДивы;<\/p>\r\n<p>- возможность получить индивидуальную дистанционную консультацию с КиберДивой (1 час). &nbsp; &nbsp;<\/p>\r\n<p>&nbsp;<\/p>\r\n<p><em>*Внимание! Транскрибация вебинара высылается в течение 7 дней после окончания мероприятия.<\/em><\/p>",
         "get_crowd_user_count": 0}]},
     {"id": 49, "image_link": "https:\/\/lsg.ru\/storage\/blog_img\/sf6prGcAN18PeRBDUssUmU7iIv1TIbfcjV4076kf.jpeg",
      "name": "Физика накануне прорыва: кризис теории и точки роста", "sum_now": 161, "start_date": "2020-10-27",
      "live_status": 0, "zoom_text": "Комната еще не активна", "get_crowd_reward": [
         {"id": 99, "lot_id": 49, "min_price": 2, "max_price": 19, "name": "Вариант №1",
          "description": "<p><strong>Позволяет: <\/strong><\/p>\r\n<p>- участвовать в трансляции;<\/p>\r\n<p>- получить записи стрима;<\/p>\r\n<p>- задавать вопросы в чате. &nbsp;<\/p>\r\n<p>&nbsp;<\/p>\r\n<p><em>*Внимание! Если Вы выбираете этот вариант и донатите свыше 20 евро, то система на вариант №2 доната автоматически не переводит<\/em><\/p>",
          "get_crowd_user_count": 41},
         {"id": 100, "lot_id": 49, "min_price": 20, "max_price": 1000, "name": "Вариант №2",
          "description": "<p><strong>Позволяет:<\/strong><\/p>\r\n<div>- участвовать в трансляции;<\/div>\r\n<div>- получить записи стрима;<\/div>\r\n<div>- задавать вопросы в чате;<\/div>\r\n<div>- получить транскрибации стрима в формате pdf (текстовая стенография стрима, обработанная профессиональным специалистом).<\/div>\r\n<div>&nbsp;<\/div>\r\n<p><em>*Запись стрима станет доступна донатерам в течение 72 часов после окончания мероприятия, а её транскрибация будет предоставлена не позднее 7 дней после завершения стрима<\/em><\/p>",
          "get_crowd_user_count": 2}]},
     {"id": 65, "image_link": "https:\/\/lsg.ru\/storage\/crowd\/LmtLBMA3OUujHHVR0djuctGrCgYqNE3jwFHBQ8gE.jpeg",
      "name": "ПОЧЕМУ COVID-19 НЕ СМОГ ОБЕСПЕЧИТЬ ОБЕЩАННЫЕ УРОВНИ СВЕРХСМЕРТНОСТИ", "sum_now": 380,
      "start_date": "2021-02-01", "live_status": 0, "zoom_text": "Комната еще не активна", "get_crowd_reward": [
         {"id": 110, "lot_id": 65, "min_price": 2, "max_price": 19, "name": "Вариант №1",
          "description": "<p><strong>Позволяет: <\/strong><\/p>\r\n<p>- участвовать в трансляции;<br \/>- получить записи стрима;<br \/>- задавать вопросы в чате. &nbsp;<\/p>\r\n<p>&nbsp;<\/p>\r\n<p><em>*Внимание! Если Вы выбираете этот вариант и донатите свыше 20 евро, то система на вариант №2 доната автоматически не переводит.&nbsp;Запись стрима станет доступна донатерам в течение 72 часов после окончания мероприятия<\/em><\/p>",
          "get_crowd_user_count": 89},
         {"id": 111, "lot_id": 65, "min_price": 20, "max_price": 999, "name": "Вариант №2",
          "description": "<p><strong>Позволяет:<\/strong><\/p>\r\n<div>- участвовать в трансляции;<\/div>\r\n<div>- получить записи стрима;<\/div>\r\n<div>- задавать вопросы в чате;<\/div>\r\n<div>- получить транскрибации стрима в формате pdf (текстовая стенография стрима, обработанная профессиональным специалистом).<\/div>\r\n<div>&nbsp;<\/div>\r\n<p><em>*Запись и её транскрибация будет предоставлена не позднее 7 дней после завершения стрима<\/em><\/p>",
          "get_crowd_user_count": 6}]}]
