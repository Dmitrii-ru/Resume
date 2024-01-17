from django.urls import path
from . import views

from django.contrib.auth import views as authViews
from .views import CustomLogoutView
from .forms import AuthForm

app_name = 'user_urls'
urlpatterns = [
    path('reg/', views.register, name='reg'),
    path('login/', authViews.LoginView.as_view(template_name='user_app/user.html',
                                               authentication_form=AuthForm), name='user'),
    path('exit/', CustomLogoutView.as_view(template_name='user_app/exit.html',
                                               redirect_field_name='next'), name='exit'),
    path('profile/', views.profile, name='profile'),
    path('person/', views.person_area_view, name='person'),
]
