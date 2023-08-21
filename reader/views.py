import csv
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


class ReaderView(APIView):
    serializer_class = ReaderSerializer

    def post(self, request):
        data = request.data
        digits_only = re.sub(r'\D', '', data['birth_date'])
        formatted_string = digits_only[:2] + '.' + digits_only[2:4] + '.' + digits_only[4:]
        data['birth_date'] = datetime.strptime(str(formatted_string), '%d.%m.%Y').date()
        data['class_letter'] = data['class_letter'].upper()

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
        queryset = BorrowedBook.objects.filter(id=id).order_by('date')
        return queryset


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):

            file_path = f'media/import.csv'
            with open(file_path, 'wb') as file:
                for chunk in uploaded_file.chunks():
                    file.write(chunk)


            data = []
            with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    data.append(row)


            return Response({'data': data[:3], "count": len(data) - 1, 'message': 'File uploaded and processed'}, status=201)
        else:
            return Response({'message': 'Invalid file format. Only CSV files are allowed.'}, status=400)


def index(request, id=None):
    return render(request, 'reader/reader.html')
