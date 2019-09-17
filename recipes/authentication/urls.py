from django.urls import path, re_path
from .views import (
    RoleView, RoleViewRUD, LoginView, RegisterUserView,
    AccountVerificationView, ResetPasswordView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    re_path(r'^verify-account/(?:token=(?P<token>.)/)?$',
            AccountVerificationView.as_view(), name='verify-account'),
    path('reset-password/', ResetPasswordView.as_view(),
         name='reset-password-request'),
    re_path(r'^reset-password/(?:token=(?P<token>.)/)?$',
            AccountVerificationView.as_view(), name='reset-password-confirm'),
    re_path(r'^reset-password/(?:token=(?P<token>.)/)?$',
            AccountVerificationView.as_view(), name='reset-password-save'),
    path('roles/', RoleView.as_view(), name='user-role'),
    path('roles/<int:pk>/', RoleViewRUD.as_view(), name='user-role-rud'),
]
