from rest_framework import serializers
from .models import TextBook, TextBookInvent


class TextBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBook
        fields = '__all__'  # или перечислите поля, которые разрешены

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.autor = validated_data.get('autor', instance.autor)
        instance.year = validated_data.get('year', instance.year)
        instance.clas = validated_data.get('clas', instance.clas)
        instance.iteration = validated_data.get('iteration', instance.iteration)
        instance.publisher = validated_data.get('publisher', instance.publisher)

        instance.save()
        return instance


class TextBookListSerializer(serializers.ModelSerializer):
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
    inv = serializers.CharField()
    inv_count = serializers.IntegerField(required=False, default=1)


class TextBookInventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextBookInvent
        fields = ('inv', 'isbn', 'date')
