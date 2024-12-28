from django.urls import path
from . import views

urlpatterns = [
    path('', views.research, name='research'),
]
