from django.core.cache import cache


def get_or_create_number(number, code):
    t = 120
    if cache.get(number):
        cache.set(number, code, t)
        return "повторно отправлено"
    else:
        cache.get_or_set(number, code, t)
        return "отправлено"


def get_number(number):
    return cache.get(number)
