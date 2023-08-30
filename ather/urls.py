from django.urls import path
from . import views

app_name = 'ather_urls'
urlpatterns = [
    path('congratulation/<slug_person>', views.congratulation, name='congratulation'),
    path('congratulation/<slug_person>/password', views.congratulation, name='congratulation_password'),
]
