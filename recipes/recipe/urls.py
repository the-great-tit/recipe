# from django.urls import path
from rest_framework.routers import DefaultRouter

from recipes.recipe.views import RecipesView, \
    IngredientView, RecipeIngredientView, ProcedureView, \
    MealTypeView

router = DefaultRouter()
router.register(r'meal-recipes', RecipesView, basename='recipe')
router.register(r'procedures', ProcedureView, base_name='procedure')
router.register(r'ingredients', IngredientView, base_name='ingredient')
router.register(r'ingredient_list', RecipeIngredientView,
                base_name='ingredient_list')
router.register(r'meal-types', MealTypeView)
urlpatterns = router.urls
