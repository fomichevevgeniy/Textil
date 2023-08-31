
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('sklad/', sklad, name='sklad'),
    path('vyazka/', vyazka, name='vyazka'),
    path('shitye/', shitye, name='shitye'),
    path('gotovie/', gotovie, name='gotovie'),
    path('clienti/', clienti, name='clienti'),
]