from django.contrib import admin

from recipes.models import (Cart, Favorite, Ingredient, Recipe,
                            RecipeIngredient, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit']
    search_fields = ['name']


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'favorite_count']
    list_filter = ['name', 'author', 'tags']
    readonly_fields = ['favorite_count']

    def favorite_count(self, obj):
        return obj.favorite_recipe.all().count()

    favorite_count.short_description = 'Добавлено в избранное'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'recipe', 'ingredient', 'amount']


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
