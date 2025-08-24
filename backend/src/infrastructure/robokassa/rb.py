from robokassa import Robokassa

# Пример инициализации
robokassa = Robokassa(
    merchant_login='scheduler',  # Тестовый логин в Robokassa
    password1='Y60gw5TNW5QQQEHW0xwA',  # Тестовый пароль 1
    password2='mTzin47qj9GfK9J5KvNR',  # Тестовый пароль 2
    is_test=True,  # Включаем тестовый режим
)

# Генерация ссылки на тестовый платеж
response = robokassa.generate_open_payment_link(
    out_sum=1.0,  # Сумма платежа
    inv_id=123,  # Номер счета (invoice ID)
    description='ttt',
)

# Получаем ссылку из объекта ответа (RobokassaResponse)
payment_url = response.url

print('Ссылка на тестовый платеж:', payment_url)
