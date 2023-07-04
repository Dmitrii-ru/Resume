from django.core.cache import cache

from resume.models import AboutMe, MyEducation, Stack

cache_dict = {'AboutMe': {
              'about_me': AboutMe.objects.all().first()},

}

# cache_dict = {
#     'about_me': AboutMe.objects.all().first(),
#     'my_education': MyEducation.objects.all(),
#     'stacks': Stack.objects.all(),
# }


cache_dict_time = {
    'about_me': 10,
    'my_education': 10,
    'stacks': 10,
}


def get_cache(model, name):
    cache_qs = cache.get(model[name])
    if not cache_qs:
        cache_qs = cache.set(model[name], cache_dict[model[name]], 10)
    return cache_qs

# def get_cache(name):
#     cache_qs = cache.get(name)
#     if not cache_qs:
#         cache.set(name, cache_dict[name], 10)
#         cache_qs = cache.get(name)
#     return cache_qs
