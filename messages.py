

help_message = '''
Отправьте команду /buy, чтобы перейти к покупке.
/1
/pay
/subsribe
/new
/all
'''

start_message = 'Привет! Это бот, соданный @dimaystinov для оплаты стримов от Витальича\n' + help_message

pre_buy_demo_alert = '''\
Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карточку с номером `4242 4242 4242 4242`
Счёт для оплаты:
'''

terms = '''
'''

donat_title = 'Спонсировать стрим'
donat_description = '''
Спасибо за выбор стрима `{title}` на сумму `{total_amount} {currency}`
'''

AU_error = '''\
Ошибка
'''

wrong_email = '''\
Нам кажется, что указанный имейл не действителен.
Попробуйте указать другой имейл
'''

successful_payment = '''
Платеж на сумму `{total_amount} {currency}` совершен успешно! Ссылка на трансляцию придёт сюда как только она начнётся!
Правила возврата средств смотрите в /terms
'''

MESSAGES = {
    'start': start_message,
    'help': help_message,
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'terms': terms,
    'donat_title': donat_title,
    'donat_description': donat_description,
    'AU_error': AU_error,
    'wrong_email': wrong_email,
    'successful_payment': successful_payment,
}

