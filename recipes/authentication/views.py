from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from jwt import ExpiredSignatureError, DecodeError
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .utils.mails import auth_email

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views, status, viewsets

from recipes.authentication.serializers import \
    RoleSerializer, RegisterSerializer, CountrySerializer

from recipes.authentication.models import Role, Country

User = get_user_model()


class RoleView(viewsets.ModelViewSet):
    # permission_classes = ()
    queryset = Role.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializer


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CountrySerializer


class RegisterUserView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = RegisterSerializer


class LoginView(views.APIView):
    permission_classes = ()

    @staticmethod
    def post(request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    response = user.gen_token
                    return Response({'token': response, 'user': {
                        'user_id': user.id,
                        'username': user.username,
                        'email': user.email,
                        # 'role': user.role.id,
                        'profile': {
                            'first_name': user.profile.first_name,
                            'other_names': user.profile.other_names,
                            'bio': user.profile.bio,
                            'phone_number': user.profile.phone_number,
                        }
                    }}, 200)
                return Response(
                    {"error": "Wrong password or username"},
                    status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({'error': 'You are not registered'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Please provide a username and '
                                      'password'},
                            status=status.HTTP_400_BAD_REQUEST)


class AccountVerificationView(views.APIView):
    permission_classes = ()

    @staticmethod
    def get(request, *args, **kwargs):
        token = request.query_params.get("token").replace('/', '').strip()
        try:
            decoded_payload = jwt_decode_handler(token)
            User.objects.filter(
                username=decoded_payload['username']
            ).update(is_active=True)
            return Response({'message': 'Account activated successfully'},
                            status=status.HTTP_200_OK)
        except ExpiredSignatureError:
            return Response({'error': 'JWT expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(views.APIView):
    permission_classes = ()

    @staticmethod
    def post(request, *args, **kwargs):
        email = request.data.get('email')

        if email:
            try:
                validate_email(email)
                user = User.objects.get(email=email)
                token = user.gen_token
                auth_email.delay(
                    user.email,
                    'Reset your Recipes password',
                    'mail_templates/reset_password.html',
                    token
                )
                return Response({'message': 'Reset password email sent'},
                                status=status.HTTP_200_OK)
            except ValidationError:
                return Response({'error': 'Invalid email format'},
                                status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({'error': 'That email is not registered'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Please provide an email'},
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request, *args, **kwargs):
        try:
            token = request.query_params.get("token").replace('/', '').strip()
            jwt_decode_handler(token)
            return Response({'message': 'You can now enter '
                                        'your new password'},
                            status=status.HTTP_200_OK)
        except ExpiredSignatureError:
            return Response({'error': 'JWT expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({'error': 'Invalid url. Token parameter is '
                                      'required'},
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, *args, **kwargs):
        try:
            token = request.query_params.get("token").replace('/', '').strip()
            decoded_payload = jwt_decode_handler(token)
            password = request.data.get('password')
            if password:
                if len(password) < 8:
                    return Response({'error': 'Password has to be at least '
                                              '8 characters long'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.get(
                        username=decoded_payload['username']
                    )
                    user.set_password(password)
                    user.save()
                    return Response({'message': 'Password reset '
                                                'successfully'},
                                    status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Please enter your new password'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ExpiredSignatureError:
            return Response({'error': 'JWT expired'},
                            status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({'error': 'Invalid url. Token parameter is '
                                      'required'},
                            status=status.HTTP_400_BAD_REQUEST)
