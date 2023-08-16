import os

from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import TextBook, TextBookInvent, TextBookArhiv
import qrcode
from .serializer import TextBookSerializer, TextBookInventSerializer, InventSerializer, TextBookListSerializer


class TextBooksList(ModelViewSet):
    queryset = TextBook.objects.all().order_by('clas', 'title')
    serializer_class = TextBookListSerializer


class TextBookView(APIView):
    serializer_class = TextBookSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': 'ISBN already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, isbn):
        try:
            instance = TextBook.objects.get(isbn=isbn)
        except TextBook.DoesNotExist:
            return Response({'error': 'TextBook not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        try:
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response({'error': 'ISBN already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

            last_inv = TextBookInvent.objects.filter(isbn=isbn, inv__startswith=str(inv)).order_by('-inv').first()

            if last_inv is not None:
                parts = last_inv.inv.split('.')
                last_number = int(parts[-1])
            else:
                last_number = 0

            qol = last_number + (inv_count or 1)

            # Цикл создания записей и генерации QR-кодов
            for n in range(last_number, qol):
                nuls = str((n + 1))
                nuls = "0" * (3 - len(nuls)) + nuls
                new_inv = str(inv) + '.' + nuls

                textbook = get_object_or_404(TextBook, isbn=isbn)

                inventiveness = TextBookInvent(inv=new_inv, isbn=textbook)
                inventiveness.save()

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

                media_path = os.path.join(os.getcwd(), 'media')
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
            invs = TextBookInvent.objects.filter(isbn=isbn).order_by('inv')
            serialize_invent_data = [{'inv': inv.inv, 'isbn': inv.isbn.isbn, 'date': inv.date} for inv in invs]
            return Response({'message': 'Запись успешно создана', 'invs': serialize_invent_data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        serializer = InventSerializer(data=request.data)

        isbn = request.data.get('isbn')
        inv = request.data.get('inv')
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


def index(request, isbn=None):
    return render(request, 'textbook/textbook.html')