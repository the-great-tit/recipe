from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Role

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
