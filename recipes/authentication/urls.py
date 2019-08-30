from django.urls import path, re_path
from .views import (
    RoleView, RoleViewRUD, LoginView, RegisterUserView, AccountVerificationView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    re_path(r'^verify-account/(?:token=(?P<token>.)/)?$',
            AccountVerificationView.as_view(), name='verify-account'),
    path('roles/', RoleView.as_view(), name='user-role'),
    path('roles/<int:pk>/', RoleViewRUD.as_view(), name='user-role-rud'),
]
