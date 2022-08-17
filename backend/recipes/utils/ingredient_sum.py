from django.db.models import F, Sum

from recipes.models import Recipe


def get_ingredient_sum(request):
    user = request.user
    recipes_in_cart = Recipe.objects.filter(cart_recipe__user=user)
    result_data = recipes_in_cart.values_list(
        'recipe_ingredient__ingredient__name',
        'recipe_ingredient__ingredient__measurement_unit',
    ).annotate(Sum('recipe_ingredient__amount'))
    return result_data
