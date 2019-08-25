from django.contrib import admin
from django.urls import path, include

api_url_patterns = [
    path('auth/', include('recipes.authentication.urls')),
    path('recipes/', include('recipes.recipe.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_url_patterns))
]
