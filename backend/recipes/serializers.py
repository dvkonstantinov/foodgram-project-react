from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField

from users.serializers import UserSerializer

from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class AddIngredientsToRecipeSerializer(serializers.ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']


class GetRetrieveIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True,
                                            source='ingredient.id')
    name = serializers.CharField(read_only=True,
                                 source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id',
                  'name',
                  'measurement_unit',
                  'amount'
                  ]

    def get_amount(self, obj):
        print(obj)
        amount = RecipeIngredient.objects.filter(recipe=obj)
        print(amount)


class RecipeDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    def get_ingredients(self, obj):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return GetRetrieveIngredientSerializer(recipe_ingredients,
                                               many=True).data

    def get_is_favorited(self, obj):
        request = self.context['request']
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            recipe=obj,
            user=self.context['request'].user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        if not request or request.user.is_anonymous:
            return False
        return Cart.objects.filter(
            recipe=obj,
            user=self.context['request'].user).exists()

    class Meta:
        model = Recipe
        fields = ['id',
                  'tags',
                  'ingredients',
                  'author',
                  'name',
                  'text',
                  'image',
                  'cooking_time',
                  'is_favorited',
                  'is_in_shopping_cart',
                  ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    ingredients = AddIngredientsToRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'name',
            'ingredients',
            'tags',
            'image',
            'tags',
            'text',
            'cooking_time',
            'author',
        ]

    @staticmethod
    def set_ingredients(recipe, ingredients_data):
        for ingredient in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient['id'],
                                            amount=ingredient['amount'])

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.set_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, recipe, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        for attr, value in validated_data.items():
            setattr(recipe, attr, value)
        recipe.save()
        recipe.tags.set(tags_data)
        recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe)
        recipe_ingredient.delete()
        self.set_ingredients(recipe, ingredients_data)
        return recipe

    def to_representation(self, recipe):
        data = RecipeDetailSerializer(
            recipe,
            context={'request': self.context.get('request')}).data
        return data


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time'
        ]
