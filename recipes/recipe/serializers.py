from rest_framework import serializers

from recipes.recipe.models import \
    Recipe, Procedure, Ingredient, RecipeIngredient, MealType


class RecipeSerializers(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField('get_procedures')
    ingredients = serializers.SerializerMethodField('get_ingredients')

    class Meta:
        model = Recipe
        fields = ["id", "title", "description", "prep_time", "cook_time",
                  "images", "published", "meal_culture", "meal_type",
                  "author", "country", "steps", "ingredients"]
        read_only_fields = ["author", "published"]

    def get_procedures(self, obj):
        steps = Procedure.objects.filter(recipe_id=obj.id)
        return [{'id': step.get('id'), 'steps': step.get('steps')}
                for step in steps.values()]

    def get_ingredients(self, ingr):
        ingredients = RecipeIngredient.objects.filter(recipe_id=ingr.id)
        return [{'id': ingr.get('id'),
                 'ingredient': ingr.get('ingredients_list')}
                for ingr in ingredients.values()]


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ["id", "recipe", "steps"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredients_list", "recipe"]


class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = ["id", "name"]
