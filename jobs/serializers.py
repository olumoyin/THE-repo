from rest_framework import serializers
from .models import Industry

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name']


class CreateIndustrySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        """
        Create and return a new Industry instance, given the validated data.
        """
        return Industry.objects.create(**validated_data)