from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from users.views import SubscriptionViewSet, UserViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users/subscriptions', SubscriptionViewSet,
                basename='subscriptions')
# router.register(r'users/(?P<user_id>\d+)/subscribe', UserViewSet,
#                 basename='subscribe')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    # path('users/<int:pk>/subscribe/', subscribe_author,
    #      name='subscribe_author'),
    # path('users/<int:pk>/subscribe/', subscribe_author,
    #      name='subscribe_author'),
    path('auth/token/login/', TokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
]
