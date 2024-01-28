# User Registration by Phone Number

## Request: POST /api/verification_phone/send_code

### Validation

- Check phone number format.
- Check phone number uniqueness.

### Functions

- Simulate code send delay.
- Generate code.
- Cache code.

### Response

- Confirmation code

---

# User Creation and [Invitation]() Issuance

## Request: POST /api/verification_phone/<invite_code>

### Validation

- Check phone number format.
- Check phone number uniqueness.
- Check code presence in cache.

### Functions

- Create user.
- Generate invitation.
- Generate link to user profile.

### Response

- Link to user profile
- Invitation

---

# Invitation Activation

## Request: PUT /api/verification_phone/profile/<phone_number>

### Validation

- Check invitation existence.

### Functions

- Check profile existence.
- Check invitation activation.
- Activate invitation.

### Response

- User successfully activated invite

---

# List Invitations

## Request: GET /api/verification_phone/profile/<phone_number>

### Functions

- Check profile existence.
- Get a list of users who activated the invite of the current user.

### Response

- Profile
- List of invitations


### Функционал
- Авторизация по номеру телефона. Первый запрос на ввод номера телефона. Имитировать отправку 4хзначного кода авторизации(задержку на сервере 1-2 сек). Второй запрос на ввод кода
- Если пользователь ранее не авторизовывался, то записать его в бд
- Запрос на профиль пользователя
- Пользователю нужно при первой авторизации нужно присвоить рандомно сгенерированный 6-значный инвайт-код(цифры и символы)
- В профиле у пользователя должна быть возможность ввести чужой инвайт-код(при вводе проверять на существование). В своем профиле можно активировать только 1 инвайт код, если пользователь уже когда-то активировал инвайт код, то нужно выводить его в соответсвующем поле в запросе на профиль пользователя
- В API профиля должен выводиться список пользователей(номеров телефона), которые ввели инвайт код текущего пользователя.