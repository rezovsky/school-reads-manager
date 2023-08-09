from rest_framework import serializers
from .models import TextBook, TextBookInvent


class TextBookSerializer(serializers.ModelSerializer):
    invent_count = serializers.SerializerMethodField()

    class Meta:
        model = TextBook
        fields = ['isbn', 'title', 'autor', 'year', 'clas', 'publisher', 'invent_count']

    def get_invent_count(self, obj):
        return TextBookInvent.objects.filter(isbn=obj.isbn).count()


class TextBookInventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBookInvent
        fields = ('inv', 'isbn', 'date')
