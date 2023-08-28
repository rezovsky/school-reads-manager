from rest_framework import serializers

from reader.models import Reader, BorrowedBook


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.clas = validated_data.get('clas', instance.clas)
        instance.class_letter = validated_data.get('class_letter', instance.class_letter)

        instance.save()
        return instance


class ReadersListSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Reader
        fields = ('id', 'data')

    def get_data(self, obj):
        return {
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "birth_date": obj.birth_date,
            "clas": obj.clas,
            "class_letter": obj.class_letter,
        }


class ReaderBorrowedBooksSerializer(serializers.ModelSerializer):
    textbook_title = serializers.SerializerMethodField()

    class Meta:
        model = BorrowedBook
        fields = ('id', 'reader', 'textbook', 'textbook_title')

    def get_textbook_title(self, obj):
        return obj.textbook.isbn.title if obj.textbook.isbn else None


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = '__all__'
