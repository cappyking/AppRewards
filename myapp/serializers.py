from rest_framework import serializers
from myapp.models import *
from django.contrib.auth.models import User


class AppLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTaskHolder
        fields = '__all__'


class ImageUploadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MasterTaskHolder
        fields = (
            'title','image'
        )
    def update(self, instance: MasterTaskHolder, validated_data):
        instance.image = validated_data['image']
        instance.status='C'
        instance.save()
        return instance

# Serialser for sending app details without authentication
class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppLib
        fields = '__all__'

# User Serializer for login
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class AdminTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppLib
        fields = ('title', 'point', 'applink', 'category')


# Register Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

        return user
