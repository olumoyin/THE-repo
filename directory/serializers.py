from rest_framework import serializers

from directory.models import ServiceLocation
from users.models import CompanyProfile


class ServiceLocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLocation
        fields = "__all__"

    # Checks if user is an organisation then creates a new service location object
    #  using validated data
    def create(self, validated_data):
        user = self.context['request'].user
        try:
            operator = CompanyProfile.objects.get(organisation=user)
        except:
            raise serializers.ValidationError("You don't have permission to create a service location because you are not a WISP Operator.")
        
        service_location = ServiceLocation.objects.create(
                description = validated_data['description'],
                latitude =validated_data['latitude'],
                longitude = validated_data['longitude'],
                service = validated_data['service'],
                speed = validated_data['speed'],
                operator = operator,
    )
        return service_location

class ServiceLocationSerializer(serializers.ModelSerializer):
    sl_operator_info = serializers.SerializerMethodField()


    class Meta:
        model = ServiceLocation
        fields = "__all__"
        fields = ['id', 'description', 'address', 'latitude', 'longitude', 'service', 'speed', 'sl_operator_info']
    
    def get_sl_operator_info(self, obj):
        try:
            operator = obj.operator
            return SlOperatorSerializer(operator).data
        except:
            return None
    
class SlOperatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ["id", "name", "brand_logo"]

