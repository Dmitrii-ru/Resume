from django.core.cache import cache
import redis
from django.shortcuts import get_object_or_404

from resume.models import AboutMe, MyEducation, Stack, Projects, CardProject


cache_dict = {
    'index_key': {
        'about_me': AboutMe.objects.all().first(),
        'my_education': MyEducation.objects.all(),
        'stacks_all': Stack.objects.all(),
    },
    'project_key': {
        'projects_all': Projects.objects.all(),
        'cards_all': CardProject.objects.select_related('project').all(),
    },
}

def update_model_cache(model, name):
    model_cache = cache.get_or_set(model, cache_dict[model], 5)

    if not model_cache.get(name):
        print(name)
        model_cache.update({name: cache_dict[model][name]})
        cache.set(model, model_cache)


def get_cache_resume(model, name):
    update_model_cache(model, name)
    return cache.get(model)[name]


def get_filter_cards(model, name, project):
    update_model_cache(model, name)
    model_cache = cache.get(model)
    if not model_cache.get(project.id):
        model_cache.update(
            {project.id: list(cache.get(model)[name].filter(project=project).values_list('id', flat=True))}
        )
        cache.set(model, model_cache)
    card_ids = model_cache[project.id]
    return [card for card in cache.get(model)[name] if card.id in card_ids]


def get_filter_stacks(model, name, project):
    update_model_cache(model, name)
    model_cache = cache.get(model)
    if not model_cache.get(project.id):
        model_cache.update(
            {project.id: list(project.prod_stack.all().values_list('id', flat=True))}
        )
        cache.set(model, model_cache)
    stacks_ids = model_cache[project.id]
    return [stack for stack in cache.get(model)[name] if stack.id in stacks_ids]




# def get_filter_cards(model, name, project):
#     update_model_cache(model, name)
#     cards = cache.get(f"{model}_{name}_{project.id}")
#     if cards is None:
#         model_cache = cache.get(model)
#         if not model_cache.get(project.id):
#             model_cache.update({project.id: cache.get(model)[name].filter(project=project).values_list('id', flat=True)})
#             cache.set(model, model_cache)
#         card_ids = model_cache[project.id]
#         cards = cache.get(model)[name].filter(id__in=card_ids)
#         cache.set(f"{model}_{name}_{project.id}", cards)
#     return cards
