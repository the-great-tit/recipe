"""Recipe, Ingredients, procedures."""
import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from soft_delete_it.models import SoftDeleteModel
from recipes.authentication.models import User


class MealType(SoftDeleteModel):
    """Meal type(eg. desert)."""

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        """Display name by default."""
        return self.name


class MealTime(SoftDeleteModel):
    """Meal time (eg. breakfast, lunch, dinner)
    """
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Country(SoftDeleteModel):
    """Countries cultures
    """
    name = models.CharField(max_length=244)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class MealCulture(SoftDeleteModel):
    """Culture category for the meal
    """
    culture = models.CharField(max_length=244, default='Native')
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, null=True)


class Recipe(SoftDeleteModel):
    """Recipe data."""

    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    GUID = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    prep_time = models.CharField(max_length=50)
    cook_time = models.CharField(max_length=50)
    images = ArrayField(
        models.CharField(max_length=500, blank=True),
        size=8,
    )
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    meal_type = models.ForeignKey(
        MealType, on_delete=models.DO_NOTHING, null=True)
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.DO_NOTHING)
    meal_culture = models.ManyToManyField(MealCulture)


class Ingredient(SoftDeleteModel):
    """Ingredients (eg. salt)."""

    name = models.CharField(max_length=100)
    recipe_ingredient = models.ManyToManyField(
        Recipe, through='RecipeIngredient')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        """Display name by default."""
        return self.name


class Procedure(SoftDeleteModel):
    """Link recipes to ingredients and making specifications like quantity."""

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    body = models.TextField(max_length=1500)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)


class RecipeIngredient(SoftDeleteModel):
    """Link recipes to ingredients and making specifications like quantity."""

    quantity = models.FloatField()
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING, null=True)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.DO_NOTHING, null=True)
