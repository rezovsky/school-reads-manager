from rest_framework import serializers

from reader.models import Reader


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
