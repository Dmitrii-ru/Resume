from django.core.cache import cache
import redis
from django.shortcuts import get_object_or_404
from django_redis import get_redis_connection


def get_model_all(model):
    return cache.get_or_set(f'{model._meta.model_name}_all', model.objects.all(), 30)


def get_model_all_order(model, order):
    return cache.get_or_set(f'{model._meta.model_name}_all_order{order}', model.objects.all().order_by(order), 30)


def get_single_model_obj(model, field, value):
    cache_key = cache.get_or_set(f'{model._meta.model_name}_get_{field}', {}, 30)
    if cache_key.get(value) is None:
        kwargs = {field: value}
        new_obj = get_object_or_404(model, **kwargs)
        cache_key[value] = new_obj
        cache.set(f'{model._meta.model_name}_get_{field}', cache_key)
    return cache_key.get(value)


def get_filter_model(model, field, value):
    cache_key = cache.get_or_set(f'{model._meta.model_name}_filter_{field}', {}, 30)
    if cache_key.get(value) is None:
        kwargs = {field: value}
        new_obj = model.objects.filter(**kwargs)
        cache_key[value] = new_obj
        cache.set(f'{model._meta.model_name}_filter_{field}', cache_key)
    return cache_key.get(value)


def get_mtm_all(model, field, value):
    cache_key = cache.get_or_set(f'{model._meta.model_name}_mtm_{field}', {}, 30)
    if cache_key.get(value.id) is None:
        new_obj = getattr(value, f'{field}').all()
        cache_key[value.id] = new_obj
        cache.set(f'{model._meta.model_name}_mtm_{field}', cache_key)
    return cache_key.get(value.id)


def delete_cache(model):
    redis_client = redis.Redis(host='localhost', port=6379, db=1, charset="utf-8", decode_responses=True)
    keys = redis_client.keys('*')
    for key in keys:
        if model in key:
            redis_client.delete(key)


def count_send_email(ip):
    if not ip:
        return 3
    ip_data = cache.get('ip_data', {})
    client = ip_data.get(ip, 0)
    return client


def update_cache_ip(ip):
    if ip:
        ip_data = cache.get('ip_data', {})
        ip_data[ip] = ip_data.get(ip, 0) + 1
        cache.set('ip_data', ip_data)


def del_ip_all():
    cache.delete('ip_data')


def count_visit():
    db2 = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)
    return db2.dbsize()
