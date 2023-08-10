from rest_framework import serializers
from .models import TextBook, TextBookInvent


class TextBookSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = TextBook
        fields = ('isbn', 'data')

    def get_data(self, obj):
        invent_count = TextBookInvent.objects.filter(isbn=obj.isbn).count()
        return {
            "title": obj.title,
            "autor": obj.autor,
            "year": obj.year,
            "clas": obj.clas,
            "publisher": obj.publisher,
            "invent_count": invent_count,
        }


class InventSerializer(serializers.Serializer):
    isbn = serializers.CharField()
    inv = serializers.IntegerField()
    inv_count = serializers.IntegerField(required=False, default=1)


class TextBookInventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBookInvent
        fields = ('inv', 'isbn', 'date')
