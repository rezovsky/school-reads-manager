import csv
import hashlib
import os
import re
from datetime import datetime

from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from reader.models import Reader, BorrowedBook
from reader.serializer import ReaderSerializer, ReadersListSerializer, ReaderBorrowedBooksSerializer


class ReadersList(ModelViewSet):
    queryset = Reader.objects.all().order_by('last_name', 'first_name')
    serializer_class = ReadersListSerializer

    def list(self, request, *args, **kwargs):
        # Получаем данные из базы данных с помощью queryset и сериализуем их
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        class_combinations = set()

        # Перебираем queryset и добавляем уникальные сочетания в множество
        for reader in queryset:
            class_combinations.add(f"{reader.clas} {reader.class_letter}")

        # Преобразуем множество обратно в список
        group = sorted(list(class_combinations))

        # Комбинируем данные сериализатора и дополнительную информацию
        data = {
            'readers': serializer.data,
            'groups': group,
            'total_readers': queryset.count(),
        }

        return Response(data)


class ReaderView(APIView):
    serializer_class = ReaderSerializer

    def post(self, request):
        data = request.data
        digits_only = re.sub(r'\D', '', data['birth_date'])
        formatted_string = digits_only[:2] + '.' + digits_only[2:4] + '.' + digits_only[4:]
        data['birth_date'] = datetime.strptime(str(formatted_string), '%d.%m.%Y').date()
        data['class_letter'] = data['class_letter'].upper()
        data['first_name'] = data['first_name'].capitalize()
        data['last_name'] = data['last_name'].capitalize()

        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': 'ID already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReaderBorrowedBookList(generics.ListAPIView):
    serializer_class = ReaderBorrowedBooksSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        queryset = BorrowedBook.objects.filter(id=id).order_by('date').select_related('textbook__isbn')
        return queryset


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)
    serializer_class = ReaderSerializer

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):

            media_path = os.path.join(os.getcwd(), 'media')
            if not os.path.isdir(media_path):
                os.mkdir(media_path)

            file_path = os.path.join(media_path, 'import.csv')

            with open(file_path, 'wb') as file:
                for chunk in uploaded_file.chunks():
                    file.write(chunk)

            data = self.read_data_from_file(file_path)

            key = self.calculate_file_hash(file_path)

            return Response(
                {'data': data[:3], "count": len(data) - 1, "key": key, 'message': 'File uploaded and processed'},
                status=201)
        else:
            return Response({'message': 'Invalid file format. Only CSV files are allowed.'}, status=400)

    def get(self, request, *args, **kwargs):
        key = request.GET.get('key')

        file_path = os.path.join(os.getcwd(), 'media', 'import.csv')
        file_key = self.calculate_file_hash(file_path)

        if key == file_key:
            data = self.read_data_from_file(file_path)
            for row in data:
                last_name = row[0].capitalize()
                first_name = row[1].capitalize()
                birth_date = datetime.strptime(row[2], '%m/%d/%Y').date()
                clas = int(row[3])
                class_letter = row[4].upper()

                serializer = self.serializer_class(data={
                    'first_name': first_name,
                    'last_name': last_name,
                    'birth_date': birth_date,
                    'clas': clas,
                    'class_letter': class_letter
                })

                if serializer.is_valid():
                    obj, created = Reader.objects.get_or_create(
                        first_name=first_name,
                        last_name=last_name,
                        birth_date=birth_date,
                        clas=clas,
                        class_letter=class_letter
                    )

        response_data = {'message': 'GET request successful', }
        return Response(response_data)

    def calculate_file_hash(self, file_path, hash_algorithm="sha256"):
        hash_obj = hashlib.new(hash_algorithm)
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    def read_data_from_file(self, file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                data.append(row)
        return data


def index(request, id=None):
    return render(request, 'reader/reader.html')
