from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.pagination import CustomPagination
from .models import Subscription, User
from .serializers import (PasswordChangeSerializer, SubscribeSerializer,
                          UserCreateSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        queryset = User.objects.all()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["get"],
        detail=False,
        url_path="me",
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def user_own_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["post"],
        detail=False,
        url_path="set_password",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=PasswordChangeSerializer,
    )
    def change_password(self, request):
        user = self.request.user
        print(user)
        serializer = self.get_serializer(
            data=request.data
        )
        if serializer.is_valid():
            if not user.check_password(serializer.data.get(
                    "current_password")):
                return Response(
                    {"current_password": ["Указан неверный текущий пароль."]},
                    status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({'message': 'Пароль успешно изменен.'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path="subscribe",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=SubscribeSerializer,
    )
    def subscribe_author(self, request, pk=None):
        user = get_object_or_404(User, email=request.user.email)
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            if user.id == author.id:
                return Response(
                    {'errors': 'Нельзя подписываться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST)
            _, created = Subscription.objects.get_or_create(user=user,
                                                            author=author)
            if created:
                serializer = SubscribeSerializer(
                    author,
                    context={'request': request}
                )
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'errors': 'Вы уже подписаны на этого автора'},
                                status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            try:
                subscription = Subscription.objects.get(user=user,
                                                        author=author)
            except ObjectDoesNotExist:
                return Response({'errors': 'Ошибка отписки. Возможно вы не '
                                           'подписаны на данного'
                                           'пользователя'},
                                status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response({'success': 'Вы отписались от пользователя'},
                            status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(author__user=self.request.user)
