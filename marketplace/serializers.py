from rest_framework import serializers
from .models import UserModel, JobPost
from django.contrib.auth.models import User as AuthUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = UserModel
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(max_length=15, required=True)
    location = serializers.CharField(max_length=100, required=True)
    role = serializers.ChoiceField(choices=['Freelancer', 'Client', 'Admin'], required=False, default='Client')

    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'phone_number', 'location', 'role',]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        # Check if password and confirm_password match
        if password != confirm_password:
            raise serializers.ValidationError({"error": "Passwords don't match."})

        # Check if email already exists
        email = attrs.get('email')
        if AuthUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email already exists."})

        return attrs

    def create(self, validated_data):
        # Extracting user data
        user_data = {key: validated_data[key] for key in ['username', 'first_name', 'last_name', 'email']}
        password = validated_data.pop('password')
        
        # Creating user
        user = AuthUser(**user_data)
        user.set_password(password)
        user.is_active = False  # User needs to verify their email first
        user.save()

        # Creating student model instance
        student = UserModel.objects.create(
            user=user,
            phone_number=validated_data['phone_number'],
            location=validated_data['location'],
            role=validated_data.get('role', 'Client'),
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)



class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'