import re

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipes.recipe.serializers import RecipeSerializers, \
    IngredientSerializer, RecipeIngredientSerializer, ProcedureSerializer, \
    MealTypeSerializer
from recipes.recipe.models import Recipe, \
    Procedure, Ingredient, RecipeIngredient, MealType

from recipes.recipe.utils.utils import validation_error


class RecipesView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RecipeSerializers

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)


class ProcedureView(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProcedureSerializer

    def perform_create(self, serializer):
        try:
            recipe = self.request.data.get('recipe')
            if not recipe:
                return validation_error(
                    "Specify a recipe to add procedures")

            recipe = Recipe.objects.get(id=recipe)

            if not self.request.data.get('body'):
                return validation_error(
                    "A procedure must have content"
                )

            pattern = '[^,]+'
            steps = re.findall(pattern, self.request.data['body'])

            serializer.save(recipe=recipe, steps=steps)
        except Exception as error:
            raise error
        return super().perform_create(serializer)

    def partial_update(self, request, *args, **kwargs):
        procedure = Procedure.objects.get(pk=kwargs.get('pk'))
        pattern = '[^,]+'
        steps = re.findall(pattern, self.request.data['body'])

        procedure.steps = steps
        procedure.save(update_fields=['steps'])
        return super().partial_update(request, *args, **kwargs)


class IngredientView(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = IngredientSerializer


class RecipeIngredientView(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RecipeIngredientSerializer

    def perform_create(self, serializer):
        print(self.request.data)
        ingredient_names = self.request.data.get('recipe_ingredients')

        ingredients_list = []
        try:
            recipe = self.request.data.get('recipe')
            if not recipe:
                return validation_error(
                    "Specify a recipe to add procedures")
            if not ingredient_names:
                return validation_error(
                    "Ingredient body cannot be empty"
                )
            for ingredient_name in ingredient_names:
                ingr = ingredient_name.get('ingredient')
                Ingredient.objects.get_or_create(name=ingr)
                ingredients_list.append(ingredient_name.get('detail'))
            serializer.save(ingredients_list=ingredients_list)
        except Exception as error:
            raise error
        return super().perform_create(serializer)

    def partial_update(self, request, *args, **kwargs):
        ingredients_list = RecipeIngredient.objects.get(pk=kwargs.get('pk'))
        ingredients_list_update = self.request.data.get('ingredients_list')
        if not ingredients_list_update:
            return validation_error(
                "Ingredient body cannot be empty"
            )
        ingredients_list.ingredients_list = ingredients_list_update
        ingredients_list.save(update_fields=['ingredients_list'])
        return super().partial_update(request, *args, **kwargs)


class MealTypeView(viewsets.ModelViewSet):
    queryset = MealType.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = MealTypeSerializer
