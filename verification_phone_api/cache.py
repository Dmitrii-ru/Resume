from django.core.cache import cache


def get_or_create_number(number, code):
    t = 120
    if cache.get(number):
        cache.set(number, code, t)

    else:
        cache.get_or_set(number, code, t)



def get_number(number):
    return cache.get(number)
