from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('projects/', views.projects, name='projects'),
    path('research/', views.research, name='research'),
    path('research/<int:pk>/', views.research_detail, name='research_detail'),
    path('articles/', views.articles, name='articles'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('login/', views.login_view, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
