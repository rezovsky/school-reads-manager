import os
import random

from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .models import TextBook, TextBookInvent, TextBookArhiv
from .forms import AddTextBookForm, AddTextBookInventForm, EditTextBookForm
import datetime
import qrcode

from .serializer import TextBookSerializer, TextBookInventSerializer


class TextBookView(ModelViewSet):
    queryset = TextBook.objects.all().order_by('-date')
    serializer_class = TextBookSerializer


class TextBookInventList(generics.ListAPIView):
    serializer_class = TextBookInventSerializer

    def get_queryset(self):
        isbn = self.kwargs['isbn']
        queryset = TextBookInvent.objects.filter(isbn=isbn).order_by('inv')
        return queryset


def index(request, isbn=None):
    return render(request, 'textbook/textbook.html')
