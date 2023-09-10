from django.urls import path
from . import views

urlpatterns = [
    path('single/<str:isbn>/<str:inv>/', views.single, name='print'),
    path('multi/<str:isbn>/', views.multi, name='multi_print'),
    path('readerslist/<str:clas>/<str:letter>/', views.readerslist, name='readerslistprint'),
    path('groupbook/<str:clas>/<str:letter>/', views.groupbook, name='groupbookprint'),
]
