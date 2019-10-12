from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from .views import (RoleView, LoginView, RegisterUserView,
                    AccountVerificationView, CountryView)

router = DefaultRouter()
router.register(r'roles', RoleView)
router.register(r'countries', CountryView)

urlpatterns = router.urls
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    re_path(r'^verify-account/(?:token=(?P<token>.)/)?$',
            AccountVerificationView.as_view(), name='verify-account'),
    path(r'', include(router.urls))
]
