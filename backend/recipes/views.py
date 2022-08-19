from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.pagination import CustomPagination
from .filters import IngredientFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, Tag, Cart
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

# А если в целом, то как эта функция, как решение? Костыльно написана или
# сойдет?
    def _favorite_cart_actions(self, request, messages, model):
        user = self.request.user
        try:
            recipe = self.get_object()
        except model.DoesNotExist:
            return Response({'errors': messages['not_found']},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            _, created = model.objects.get_or_create(
                recipe=recipe,
                user=user
            )
            if created:
                serializer = ShortRecipeSerializer(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'errors': messages['already_added']},
                                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            try:
                model.objects.get(recipe=recipe, user=user).delete()
            except model.DoesNotExist:
                return Response({'errors': messages['missing']},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="favorite",
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        model = Favorite
        messages = {
            'not_found': 'Такого рецепта не сушествует',
            'already_added': 'Рецепт уже в избранном',
            'missing': 'Рецепта нет в избранном',
        }
        return self._favorite_cart_actions(request, messages, model)

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="shopping_cart",
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        model = Cart
        messages = {
            'not_found': 'Такого рецепта не сушествует',
            'already_added': 'Рецепт уже в корзине',
            'missing': 'Рецепта нет в корзине',
        }
        return self._favorite_cart_actions(request, messages, model)

    @action(
        methods=["get"],
        detail=False,
        url_path="download_shopping_cart",
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = get_ingredient_sum(request)
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = ('attachment;'
                                           'filename="inredients.txt"')
        response.write('Список ингредиентов:\n')
        for item in ingredients:
            response.write(f'{item[0]} ({item[1]}) — {item[2]}\n')
        response.write('Список сгенерирован автоматически. Foodgram')
        return response
