from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import SimpleRouter

from textbook.views import TextBookView, TextBookInventList

router = SimpleRouter()
router.register('api/textbooks', TextBookView, basename='textbooks')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('textbook/', include('textbook.urls')),
    path('book/', include('book.urls')),
    path('user/', include('user.urls')),
    path('print/', include('print.urls')),
    path('api/textbook/<str:isbn>/', TextBookInventList.as_view(), name='textbook-invent-list'),
]

urlpatterns += router.urls
urlpatterns += staticfiles_urlpatterns()
