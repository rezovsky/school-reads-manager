from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='textbook'),
path('<str:isbn>/', views.index, name='textbook-detail'),
]
