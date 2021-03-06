import config
import logging
import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types

from sqlighter import SQLighter

from lsg_parser import lsg

from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType

from messages import MESSAGES
from config import PAYMENTS_PROVIDER_TOKEN, TIME_MACHINE_IMAGE_URL
from aiogram.dispatcher.filters.state import State, StatesGroup
import keyboards as kb


# Для ввода данных в ответ на сообщения
class DataInput(StatesGroup):
    summa = State()


# задаем уровень логов
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')

# инициализируем парсер
sg = lsg()
all_id = sg.all_id()

PRICE = types.LabeledPrice(label='Донат', amount=420)


# PAY платёж ------------------------------------------------------------------
@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])

    await bot.send_invoice(message.chat.id,
                           title=MESSAGES['donat_title'],
                           description=MESSAGES['donat_description'],
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='eur',
                           photo_url=TIME_MACHINE_IMAGE_URL,
                           photo_height=512,  # !=0/None, иначе изображение не покажется
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[PRICE],
                           start_parameter='time-machine-example',
                           payload='some-invoice-payload-for-our-internal-use'
                           )


# Управление кнопками
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = int(callback_query.data.replace("btn",""))
    sg = lsg()
    variants = sg.post(code)['variants']
    #if code.isdigit():
        #code = int(code)
    await bot.send_message(callback_query.from_user.id, f'Вы выбрали id stream={code}')
    await bot.send_message(callback_query.from_user.id, 'Выберите варианты')
    await bot.send_message(callback_query.from_user.id, variants)



@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Выбрать",
                        reply_markup=kb.inline_kb[38])


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.pre_checkout_query):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            total_amount=message.successful_payment.total_amount,
            currency=message.successful_payment.currency
        )
    )


# ---------------------------------------------------------

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(MESSAGES['help'])


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые стримы и вы узнаете о них первыми =)")


@dp.message_handler(commands=['terms'])
async def process_terms_command(message: types.Message):
    await message.reply(message['terms'], reply=False)


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
async def all_id(message: types.Message):
    id_list = sg.all_id()
    for ids in id_list:
        text = sg.post(ids)
        await message.answer(ids)
        await bot.send_message(message.from_user.id, text['head'])
        await bot.send_message(message.from_user.id, str(ids),
                               reply_markup=kb.inline_kb[ids])


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
    try:
        text = sg.post(int(msg.text))
        # await bot.send_message(msg.from_user.id, "Готово")

        await bot.send_message(msg.from_user.id, text['head'])
    except:
        pass


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
