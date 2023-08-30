from django.shortcuts import render, redirect, get_object_or_404
from .models import Person, ImagesProductsShop
from ather.forms import VisitCongratulation
from user_app.user_session import UserSessionAther
from django.urls import reverse


# Create your views here.

def congratulation(request, **kwargs):
    slug = kwargs['slug_person']
    person = get_object_or_404(Person, slug=slug)
    session_ather = UserSessionAther(request)
    if not session_ather.check_person_password(slug):
        print('ss')
        return redirect('ather_urls:congratulation_password', slug)
        # return redirect('ather_urls:congratulation_password', kwargs[slug])
    images = ImagesProductsShop.objects.filter(person=person)
    context = {
        'person': person,
        'images' : images
    }
    return render(request, 'ather/congratulation.html', context=context)


def congratulation_password(request, **kwargs):
    slug = kwargs['slug_person']
    person = get_object_or_404(Person, slug=slug)

    if request.method == 'POST':
        post = request.POST.copy()
        post['password'] = person.visit_password
        form = VisitCongratulation(post)
        if form.is_valid():
            session_ather = UserSessionAther(request)
            session_ather.person_password(slug)
            return redirect('ather_urls:congratulation', slug)
    else:
        form = VisitCongratulation()
    context = {'form': form}

    return render(request, 'ather/congratulation_password.html', context=context)
