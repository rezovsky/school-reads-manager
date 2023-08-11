import os

import pytz
from django.db.models import Max
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import TextBook, TextBookInvent, TextBookArhiv
from datetime import datetime
import qrcode
from .serializer import TextBookSerializer, TextBookInventSerializer, InventSerializer


class TextBookView(ModelViewSet):
    queryset = TextBook.objects.all().order_by('clas', 'title')
    serializer_class = TextBookSerializer


class TextBookInventList(generics.ListAPIView):
    serializer_class = TextBookInventSerializer

    def get_queryset(self):
        isbn = self.kwargs['isbn']
        queryset = TextBookInvent.objects.filter(isbn=isbn).order_by('inv')
        return queryset


class InventView(APIView):
    def post(self, request, format=None):
        serializer = InventSerializer(data=request.data)
        if serializer.is_valid():
            isbn = serializer.validated_data['isbn']
            inv = serializer.validated_data['inv']
            inv_count = serializer.validated_data.get('inv_count', None)

            # Получение последнего инвентарного номера

            last_inv = TextBookInvent.objects.filter(isbn=isbn, inv__startswith=str(inv)).last().inv
            if last_inv:
                parts = last_inv.split('.')
                last_number = int(parts[-1])
            else:
                last_number = 0

            qol = last_number + (inv_count or 1)

            # Цикл создания записей и генерации QR-кодов
            for n in range(last_number, qol):
                strn = str((n + 1))
                for q in range((3 - len(strn))):
                    strn = '0' + strn
                new_inv = str(inv) + '.' + strn

                textbook = get_object_or_404(TextBook, isbn=isbn)

                texbookinvent = TextBookInvent(inv=new_inv, isbn=textbook)
                texbookinvent.save()

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=1,
                )
                qr_data = '888.' + new_inv
                qr.add_data(qr_data.replace('.', '-'))
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                media_path = os.path.join(os.getcwd(), 'bibl', 'media')
                if not os.path.isdir(media_path):
                    os.mkdir(media_path)

                qrcode_path = os.path.join(media_path, 'qrcode')
                if not os.path.isdir(qrcode_path):
                    os.mkdir(qrcode_path)

                path = os.path.join(qrcode_path, str(isbn))
                if not os.path.isdir(path):
                    os.mkdir(path)

                filename = os.path.join(path, new_inv.replace('.', '-') + ".png")
                img.save(filename)

            return Response({'message': 'Запись успешно создана', 'invs': self.serialize_invent_data(isbn)},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        serializer = InventSerializer(data=request.data)

        isbn = request.data.get('isbn')
        inv = request.data.get('inv')
        print("Type of isbn:", type(isbn))
        print("Value of isbn:", isbn)
        print("Type of inv:", type(inv))
        print("Value of inv:", inv)
        if serializer.is_valid():
            isbn = serializer.validated_data['isbn']
            inv = serializer.validated_data['inv']

            # Найдем запись в базе данных
            try:
                textbook_invent = TextBookInvent.objects.get(isbn=isbn, inv=inv)
            except TextBookInvent.DoesNotExist:
                raise Http404

            # Удаление записи
            textbook_invent.delete()

            # Получение и возвращение обновленных данных
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def serialize_invent_data(self, isbn):
        invs = TextBookInvent.objects.filter(isbn=isbn).order_by('inv')
        return [{'inv': inv.inv, 'isbn': inv.isbn.isbn, 'date': inv.date} for inv in invs]


def index(request, isbn=None):
    return render(request, 'textbook/textbook.html')
