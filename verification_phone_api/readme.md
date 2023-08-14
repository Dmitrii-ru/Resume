
# Получение кода для регистрации user по номеру телефона.
## POST api/verification_phone/send_code

## REQUEST
- body { 'phone_number' : '+7(999)999-99-99' }

### Validate
#### validate_phone_number
- Проверка формата введенного phone_number.
- Проверка на уникальность phone_number в базе данных.

### Function
- Имитация задержки отправки кода
- Генерация кода
- Кеширование кода {phone_number: code}

## RESPONSES
- Возвращаем код


---

# Заносим в базу данных user и выдаем invite.
## POST api/verification_phone/invite_code

## REQUEST
- api/verification_phone/invite_code
- body { 'phone_number' : '+7(999)999-99-99' , 'code' : '7777' }


### Validate
#### validate_phone_number
- Проверка формата введенного phone_number.
- Проверка на уникальность phone_number в базе данных.

#### validate_code
- проверка Кеш на наличие code для этого phone_number.
- проверка совпадения полученного code и core в кеш.

### Function
- Создание профиля user
- Генерация invite
- Генерация ссылки на профиль user

## RESPONSES
- Ссылка на профиль
- invite

---

# Внесение  invite
## PUT api/verification_phone/profile/<phone_number>

## REQUEST
- api/verification_phone/profile/+7(999)999-99-99
- body { 'invite' : 'HDie22' }.

### Validate

#### validate
- проверка на существование invite.

### Function
- Проверка на существование профиля.
- Проверка на активацию invite is_active = False.
- Активируем invite
- is_active = True

## RESPONSES
- "message": f"{user} successfully activated invite"

---
# Внесение  invite
## GET api/verification_phone/profile/<phone_number>

## REQUEST
- api/verification_phone/profile/+7(999)999-99-99


### Function
- Проверка на существование профиля.
- Готовим список user которые активировали invite текущего user

## RESPONSES
- Информация о профиле
- Список дубликатов user invite

