from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipes.recipe.serializers import RecipeSerializers, \
    IngredientSerializer, RecipeIngredientSerializer, ProcedureSerializer
from recipes.recipe.models import Recipe, \
    Procedure, Ingredient, RecipeIngredient


class RecipesView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RecipeSerializers


class ProcedureView(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProcedureSerializer


class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = IngredientSerializer


class RecipeIngredientView(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RecipeIngredientSerializer
