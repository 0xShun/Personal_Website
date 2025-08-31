from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('projects/', views.projects, name='projects'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('research/', views.research, name='research'),
    path('research/<int:pk>/', views.research_detail, name='research_detail'),
    path('articles/', views.articles, name='articles'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('login/', views.login_view, name='login'),
    path('comment/<str:content_type>/<int:object_id>/', views.post_comment, name='post_comment'),
]
