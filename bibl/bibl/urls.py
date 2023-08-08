from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import SimpleRouter

from textbook.views import TextBookView

router = SimpleRouter()

router.register('api/textbooks', TextBookView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('textbook/', include('textbook.urls')),
    path('book/', include('book.urls')),
    path('user/', include('user.urls')),
    path('print/', include('print.urls')),

]

urlpatterns += router.urls

urlpatterns += staticfiles_urlpatterns()

