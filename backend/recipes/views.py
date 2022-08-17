import csv

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.pagination import CustomPagination

from .filters import IngredientFilter, RecipeFilter
from .models import Cart, Favorite, Ingredient, Recipe, Tag
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortRecipeSerializer, TagSerializer)
from .utils.ingredient_sum import get_ingredient_sum


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="favorite",
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'errors': 'Такого рецепта не сушествует'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if request.method == 'POST':
            _, created = Favorite.objects.get_or_create(recipe=recipe,
                                                        user=user)
            if created:
                serializer = ShortRecipeSerializer(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'errors': 'Рецепт уже в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            try:
                Favorite.objects.get(recipe=recipe, user=user).delete()
            except ObjectDoesNotExist:
                return Response({'errors': 'Рецепта нет в избранном'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="shopping_cart",
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'errors': 'Такого рецепта не сушествует'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if request.method == 'POST':
            _, created = Cart.objects.get_or_create(recipe=recipe,
                                                    user=user)
            if created:
                serializer = ShortRecipeSerializer(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'errors': 'Рецепт уже в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            try:
                Cart.objects.get(recipe=recipe, user=user).delete()
            except ObjectDoesNotExist:
                return Response({'errors': 'Рецепта нет в корзине'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        url_path="download_shopping_cart",
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = get_ingredient_sum(request)
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = ('inline; filename="inredients.csv"')
        writer = csv.writer(response)
        writer.writerow(['Список ингредиентов:'])
        for item in ingredients:
            writer.writerow(
                [item[0], item[1], item[2]])
        writer.writerow(['Список сгенерирован автоматически. Foodgram'])
        return response
