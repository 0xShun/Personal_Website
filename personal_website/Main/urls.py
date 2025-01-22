from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('login-142004/', views.login_view, name='login'),
    path('admin-142004/', views.admin, name='admin'),
]
