from rest_framework import serializers

from recipes.recipe.models import \
    Recipe, Procedure, Ingredient, RecipeIngredient


class RecipeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"
