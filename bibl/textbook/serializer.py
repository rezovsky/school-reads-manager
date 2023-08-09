from rest_framework import serializers
from .models import TextBook, TextBookInvent


class TextBookSerializer(serializers.ModelSerializer):
    invent_count = serializers.SerializerMethodField()  # Поле для количества инвентарных номеров

    class Meta:
        model = TextBook
        fields = '__all__'  # Включите остальные поля, которые вам нужны

    def get_invent_count(self, obj):
        return TextBookInvent.objects.filter(isbn=obj.isbn).count()
