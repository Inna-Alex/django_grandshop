from rest_framework import serializers

from .models import Category, Manufactor


class ManufactorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    summary = serializers.CharField(max_length=500)

    def create(self, validated_data):
        return Manufactor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.summary = validated_data.get('summary', instance.summary)

        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'name', 'summary', 'availability')
