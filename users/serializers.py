from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError
from rest_framework import  serializers
from academy.models import StudentProfile
from .models import BaseUserProfile, CompanyProfile, User




class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type':'password'})

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_student', 'is_instructor', 'is_hirer', 'is_organisation', 'is_wisp_operator'] 

    # Validates email entered by user
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email address already exists.")
        return value
    
    # Validates password entered by user
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    # Creates a new user object using validated data
    def create(self, validated_data):
        if validated_data['is_organisation']:
            validated_data['is_hirer'] =  True

        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            
            is_student = validated_data['is_student'],
            is_instructor = validated_data['is_instructor'],
            is_hirer = validated_data['is_hirer'],

            is_organisation = validated_data['is_organisation'],
            is_wisp_operator = validated_data['is_wisp_operator'],
            

            is_verified=False

        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_student', 'is_instructor', 'is_hirer', 'is_job_hunting'] 

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class BaseUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUserProfile
        fields = "__all__"
        # exclude = ['user']

class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = "__all__"
        # exclude = ['organisation', 'id', 'updated_at']


class StudentProfileSerializer(serializers.ModelSerializer):
    '''
    A serializer for a student's profile. Only the student should have access 
    to the returned data
    '''
    user_profile_info = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = ['user_profile_info', 'bio']
    
    def get_user_profile_info(self, obj):
            try:
                profile = obj.user_profile
                return BaseUserProfileSerializer(profile).data
            except:
                return None



    
        
