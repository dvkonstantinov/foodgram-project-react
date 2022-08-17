from django.contrib import admin
from django.urls import include, path

foodgram_patterns = [
    path('', include('users.urls', namespace='users')),
    path('', include('recipes.urls', namespace='recipes')),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(foodgram_patterns))
]
