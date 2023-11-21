from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("Blog/", views.blog, name="blog"),
    path("Projects/",  views.projects, name="Projects")
]