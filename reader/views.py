from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from reader.models import Reader
from reader.serializer import ReaderSerializer


class ReadersList(ModelViewSet):
    queryset = Reader.objects.all().order_by('last_name', 'first_name')
    serializer_class = ReaderSerializer

def index(request):
    return render(request, 'reader/reader.html')
