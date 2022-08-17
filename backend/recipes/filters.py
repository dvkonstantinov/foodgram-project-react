from django_filters import rest_framework as filters

from recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(field_name='is_favorited',
                                         method='filter_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_cart'
    )
    author = filters.AllValuesFilter(field_name='author__id')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    def filter_favorite(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(favorite_recipe__user=user)
        else:
            user = self.request.user
            return queryset.exclude(favorite_recipe__user=user)

    def filter_cart(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(cart_recipe__user=user)
        else:
            user = self.request.user
            return queryset.exclude(cart_recipe__user=user)
