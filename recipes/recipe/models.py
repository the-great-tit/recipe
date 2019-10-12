"""Recipe, Ingredients, procedures."""
import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from soft_delete_it.models import SoftDeleteModel
from recipes.authentication.models import User
from recipes.authentication.models import Country


class MealType(SoftDeleteModel):
    """Meal type(eg. desert)."""

    name = models.CharField(max_length=100, unique=True)
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


class Recipe(SoftDeleteModel):
    """Recipe data."""

    title = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=500)
    GUID = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    prep_time = models.CharField(max_length=50)
    cook_time = models.CharField(max_length=50)
    images = ArrayField(
        models.CharField(max_length=500, blank=True),
        size=8, blank=True, null=True
    )
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    meal_type = models.ForeignKey(
        MealType, on_delete=models.DO_NOTHING, null=True)
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.DO_NOTHING)
    meal_culture = models.CharField(max_length=249, default="Native")
    country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, null=True)


class Ingredient(SoftDeleteModel):
    """Ingredients (eg. salt)."""

    name = models.CharField(max_length=249, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        """Display name by default."""
        return self.name


class Procedure(SoftDeleteModel):
    """Link recipes to ingredients and making specifications like quantity."""

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    body = models.TextField(max_length=15000, null=True, blank=True)
    recipe = models.OneToOneField(
        Recipe, on_delete=models.CASCADE, null=True)
    steps = ArrayField(
        models.CharField(max_length=5000, blank=True), blank=True, null=True
    )


class RecipeIngredient(SoftDeleteModel):
    """Link recipes to ingredients and making specifications like quantity."""

    ingredients_list = ArrayField(
        models.CharField(max_length=5000, blank=True), blank=True, null=True
    )
    recipe = models.OneToOneField(Recipe,
                                  on_delete=models.DO_NOTHING, null=True)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.DO_NOTHING, null=True)
