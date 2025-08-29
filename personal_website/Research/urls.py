from django.urls import path
from . import views

urlpatterns = [
    path('', views.research, name='research'),
    path('<int:paper_id>/', views.research_detail, name='research_detail'),
]
