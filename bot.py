import config
import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

from lsg_parser import lsg

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

# инициализируем парсер
sg = lsg()


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые стримы и вы узнаете о них первыми =)")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


# Команда просмотра всех постов
@dp.message_handler(commands=['all'])
async def all_posts(message: types.Message):
    text = sg.all_posts()
    for post in text:
        await message.answer(post["id"])


# новый пост
@dp.message_handler(commands=['new'])
async def new_post(message: types.Message):
    text = sg.new_id()
    print(text)
    if text:
        for id in text:
            await message.answer(id)
    else:
        await message.answer("None")


@dp.message_handler(commands=['find_post'])
async def find_post(message: types.Message):
    text = sg.new_id()
    print(text)
    if text:
        for id in text:
            await message.answer(id)
    else:
        await message.answer("None")


@dp.message_handler(commands=['pay'])
async def pay(message: types.Message):
    await message.answer("Введите id предложения")
    # bot.register_next_step_handler(message, get_name)
    id = message.text
    await message.answer("Введите сумму")
    summa = message.text
    print(id, summa, type(id))


@dp.message_handler()
async def echo_message(msg: types.Message):
    text = sg.post(int(msg.text))
    await bot.send_message(msg.from_user.id, text)


# проверяем наличие новых игр и делаем рассылки
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        # проверяем наличие новых игр
        new_id = sg.new_id()

        if sg.new_id():

            for ng in sg.new_id():

                nfo = sg.post(38)

                # получаем список подписчиков бота
                subscriptions = db.get_subscriptions()
                print(subscriptions)
                for s in subscriptions:
                    try:
                        await bot.send_message(s[1], "infa")
                    except:
                        pass
                sg.update_lastkey()
                # отправляем всем новость
        '''        with open(sg.download_image(nfo['image']), 'rb') as photo:
                    for s in subscriptions:
                        await bot.send_photo(
                            s[1],
                            photo,
                            caption=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" +
                                    nfo['link'],
                            disable_notification=True
                        )

                # обновляем ключ
                # sg.update_lastkey(nfo['id'])
'''


if __name__ == '__main__':
    # пока что оставим 10 секунд (в качестве теста)

    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(100))
    executor.start_polling(dp, skip_updates=True)

'''

1) Выбор стрима
2) Выдать картинка - кнопки выбора вариантов
3) Выбор варианта
4) Ввод прайса мин макс
5) Оплата
6) Добавление его в бд
7) Вывод успешно оплатил
8) отправить post запрос lsg максу
9) когда stream = 1 отправить ссылку

'''