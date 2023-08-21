import re
from datetime import datetime

from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from reader.models import Reader
from reader.serializer import ReaderSerializer


class ReadersList(ModelViewSet):
    queryset = Reader.objects.all().order_by('last_name', 'first_name')
    serializer_class = ReaderSerializer

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

def index(request):
    return render(request, 'reader/reader.html')
