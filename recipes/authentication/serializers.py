from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)

    user = get_user_model()

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and self.user.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                  "A user is already registered with this e-mail address.")
        return email

    def validate_username(self, username):
        if self.user.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "That username is already taken.")
        return username

    @staticmethod
    def validate_password(password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            'password': self.validated_data.get('password', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user
