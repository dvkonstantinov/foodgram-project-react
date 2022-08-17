from django.contrib import admin

from users.models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name', ]
    search_fields = ['username', 'email', ]


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'author']


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
