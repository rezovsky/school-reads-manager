from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reader'),
    path('<str:id>/', views.index, name='reader-detail'),
]
