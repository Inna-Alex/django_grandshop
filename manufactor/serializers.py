from rest_framework import serializers

from manufactor.models import Manufactor


class ManufactorSerializer(serializers.Serializer):
    # It's a kind of experiment to try another type of serializer, not the model one
    name = serializers.CharField(max_length=200)
    summary = serializers.CharField(max_length=500)

    def create(self, validated_data):
        return Manufactor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.summary = validated_data.get('summary', instance.summary)

        instance.save()
        return instance
