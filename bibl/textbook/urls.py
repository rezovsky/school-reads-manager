from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='textbook'),
    path('add', views.add, name='add'),
    path('bookedit/<str:isbn>', views.bookedit, name='bookedit'),
    path('invent', views.invent, name='invent'),
    path('<str:isbn>', views.TextBookDV, name='textbook-dv'),
    path('delbook/<str:invent>/', views.delbook, name='delbook'),
    path('arhivbook/<str:invent>/', views.arhivbook, name='arhivbook')
]
