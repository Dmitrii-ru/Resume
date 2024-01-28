# Проект: Резюме

# Приложения:
## Технологии: 
- Python, Django, Postgres, Ajax, Bootstrap, CSS, Celery, Redis, Docker, REST framework, POSTMAN.
## Реализованные решения:
- Асинхронные фоновые задачи, авторизация пользователя, кастомизация административной панели,
ручное кэширование, API, работа с session, оптимизация запросов. 
- 
## Запуск проекта
- git clone https://github.com/Dmitrii-ru/resume
- Убедитесь что в env docker_start=True
- docker-compose up --build 
- superuser = admin, password = admin 

## Приложение Резюме
### Предоставление информации о соискателе и его проектах, todo (дела на день).
### Функционал:
#### Информации о соискателе:
- Отображение информации о соискателе.
- Отправка письма со ссылкой на сайт резюме, и отправка повторно письма через 3 дня.
    - Отправка письма происходит по настройкам из базы данных.
- Список проектов.
    - Описание проекта, применяемые технологии, ссылка на сервисы.
- Список технологий.
    - Фильтрация проектов по технологиям.
- 'Ручной' cache.
#### Todo session:
- Хранения данных в session.
- Отображение календаря на месяц, перемещение по месяцам.
  - Валидация дат и дубликатов todo.
- Список актуальный todo и заверенных, изменения статуса todo.
- Удаление todo.
### Резюме API: 
- Readme: *resume_api/readme_app.md*
- Redoc:  *api/resume/docs/*
- Swagger: *api/resume/docs-swagger/*


## Приложение Блог
### Блог для обсуждения любых тем и создание постов, комментариев, like, добавление в избранное.
### Функционал:
#### Информации о соискателе:
- Авторизация пользователя.
- CRUD тем и постов, проверка прав.
- Библиотека MPTT, древовидной структура экземпляров модели, контроль уникальности название темы на одном уровне.
- Оптимизация запросов к базе данных.
- Создание slug темы как path из родителей.
- Хлебные крошки.

### В процессе
- Дописать API + Swagger

## Приложение Квиз
### Прохождение тестов, получение результатов, кастомизированная форма создания квиза в админ панели.

### Функциональные части сервиса:
- Регистрация пользователей.
- Аутентификация пользователей.
- Зарегистрированные пользователи могут проходить любой из тестовых наборов.
- Последовательный ответ на все вопросы, каждый вопрос должен выводится на новой странице с отправкой формы (перескакивать через тесты или оставлять неотмеченными нельзя).
- Не последовательный ответ на все вопросы, можно изменять ответы и передвигаться по вопросам. 
#### После завершения тестирования смотреть результат:
- Количество правильных/неправильных ответов.
- Процент правильных ответов.
- Пройти снова.

### Админка. Стандартная админка Django. Разделы:
- Стандартный раздел пользователей.
- Раздел с наборами тестов.
- Возможность на странице набора тестов добавлять вопросы/ответы к вопросам/отмечать правильные ответы.
- Валидация на то, что должен быть хотя бы 1 правильный вариант.
- Валидация на то, что все варианты не могут быть правильными.
- Удаление вопросов/вариантов ответов/изменение правильных решений при редактировании тестового набора.

## Приложение Авторизации
### Авторизация пользователя, восстановление пароля, аутентификация пользователя.  

### Функционал
- Авторизация пользователя.
- Восстановление пароля:
    - Получение ссылки для восстановления.
    - Получение настроек почти из базы данных.
- Аутентификация пользователя.
- Удаление не staff через 15 мин.
- Перенос данных session при logout.
- Сбор данных активности пользователя во всех приложениях.  
### Резюме API: 
- Readme: *user_app_api/readme_app.md*
- Redoc:  *api/user_app/docs/*
- Swagger: *api/user_app/docs-swagger/*

## Приложение Реферальная система
### Регистрация пользователя на основании invite приглашения.  

### Функционал
- Авторизация по номеру телефона. Первый запрос на ввод номера телефона. Имитировать отправку 4хзначного кода авторизации(задержку на сервере 1-2 сек). Второй запрос на ввод кода
- Если пользователь ранее не авторизовывался, то записать его в бд
- Запрос на профиль пользователя
- Пользователю нужно при первой авторизации нужно присвоить рандомно сгенерированный 6-значный инвайт-код(цифры и символы)
- В профиле у пользователя должна быть возможность ввести чужой инвайт-код(при вводе проверять на существование). В своем профиле можно активировать только 1 инвайт код, если пользователь уже когда-то активировал инвайт код, то нужно выводить его в соответсвующем поле в запросе на профиль пользователя
- В API профиля должен выводиться список пользователей(номеров телефона), которые ввели инвайт код текущего пользователя.

### Реферальная система API: 
- Readme: *verification_phone_api/readme_app.md*
- Redoc:  *api/verification_phone/docs/*
- Swagger: *api/verification_phone/docs-swagger/*

