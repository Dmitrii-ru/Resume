from django.core.cache import cache
import redis
from resume.models import AboutMe, MyEducation, Stack, Projects, CardProject

# cache_dict = {
#     'about_me': AboutMe.objects.all().first(),
#     'my_education': MyEducation.objects.all(),
#     'stacks': Stack.objects.all(),
# }
#
#
# def get_cache(name):
#     cache_qs = cache.get(name)
#     if not cache_qs:
#         cache.set(name, cache_dict[name], 1)
#         cache_qs = cache.get(name)
#     return cache_qs

cache_dict = {
    'index_key': {
        'about_me': AboutMe.objects.all().first(),
        'my_education': MyEducation.objects.all(),
        'stacks': Stack.objects.all(),
    },
    'project_key': {
        'projects': Projects.objects.all(),
        'cards': CardProject.objects.select_related('project').all(),
    }

}


# def get_cache(model, name):
#     if not cache.get(model):
#         cache.set(model, {name: cache_dict[model][name]}, 5)
#     model_cache = cache.get(model)
#     if not model_cache.get(name):
#         model_cache.update({name: cache_dict[model][name]})
#         cache.set(model, model_cache, 5)
#     return cache.get(model)[name]

def get_cache_resume(model, name):
    model_cache = cache.get_or_set(model, cache_dict[model], 5)
    if not model_cache.get(name):
        model_cache.update({name: cache_dict[model][name]})
        cache.set(model, model_cache)

    return cache.get(model)[name]
