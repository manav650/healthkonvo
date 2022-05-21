
from healthkonvo.settings import STATIC_URL
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
urlpatterns = [
    path('', views.home, name='home'),
    path('get/', views.get_bot_response, name='get_bot_response'),
]
