from django.contrib import admin
from django.urls import path, include

from recipes.recipe import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('recipes/', views.RecipesView.as_view(), name='recipes')
]
