# from django.urls import path
from rest_framework.routers import DefaultRouter

from recipes.recipe.views import RecipesView, \
    IngredientView, RecipeIngredientView, ProcedureView

router = DefaultRouter()
router.register(r'', RecipesView, basename='recipe')
router.register(r'procedure/', ProcedureView, base_name='procedure')
router.register(r'ingredient/', IngredientView, base_name='ingredient')
router.register(r'ingredient_quantity/', RecipeIngredientView,
                base_name='ingredient_quantity')
urlpatterns = router.urls

# urlpatterns = [
#     path('', RecipesView.as_view({'get': 'list',
#                                   'post': 'create'}), name='recipes'),
# ]
