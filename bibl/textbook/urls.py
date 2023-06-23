from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='textbook'),
    path('add', views.add, name='add'),
    path('invent', views.invent, name='invent'),
    path('<int:isbn>', views.TextBookDV, name='textbook-dv'),
    path('delbook/<str:invent>/', views.delbook, name='delbook'),
    path('arhivbook/<str:invent>/', views.delbook, name='arhivbook')
]
