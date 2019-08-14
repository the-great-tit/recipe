from django.urls import path
from .views import RoleView, RoleViewRUD, LoginView, RegisterUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('roles/', RoleView.as_view(), name='user-role'),
    path('roles/<int:pk>/', RoleViewRUD.as_view(), name='user-role-rud'),
]
