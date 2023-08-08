from rest_framework import serializers
from .models import TextBook


class TextBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBook
        fields = ('isbn', 'title', 'autor', 'year', 'clas', 'iteration', 'publisher', 'date')
