from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from jwt import ExpiredSignatureError, DecodeError
from rest_framework import generics, views, status
from .serializers import RoleSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler

from .models import Role

User = get_user_model()


class RoleView(generics.ListCreateAPIView):
    # permission_classes = ()
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RegisterUserView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = RegisterSerializer


class RoleViewRUD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAdmin,)
    pass


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
                        'role': user.role.id,
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
