from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import SimpleRouter

from reader.views import ReadersList, ReaderView, ReaderBorrowedBookList, FileUploadView, BorrowedBookView
from textbook.views import TextBookView, TextBookInventList, InventView, TextBooksList

router = SimpleRouter()
router.register('api/textbookslist', TextBooksList, basename='textbookslist')
router.register('api/readerslist', ReadersList, basename='readerslist')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('textbook/', include('textbook.urls')),
    path('book/', include('book.urls')),
    path('reader/', include('reader.urls')),
    path('print/', include('print.urls')),

    path('api/textbook/<str:isbn>/', TextBookInventList.as_view(), name='textbook-invent-list'),
    path('api/textbooks/', TextBookView.as_view(), name='textbook-add'),
    path('api/textbooks/<str:isbn>/', TextBookView.as_view(), name='textbook-detail'),
    path('api/invent/', InventView.as_view(), name='textbook-invent-add'),

    path('api/reader/<str:id>/', ReaderBorrowedBookList.as_view(), name='reader-list'),
    path('api/readers/', ReaderView.as_view(), name='reader-add'),
    path('api/readers/<str:id>/', ReaderView.as_view(), name='reader-detail'),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/borrowed/', BorrowedBookView.as_view(), name='borrowed-add'),
    path('api/borrowed/<int:id>/<int:reader>/', BorrowedBookView.as_view(), name='borrowed-delete')

]

urlpatterns += router.urls
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
