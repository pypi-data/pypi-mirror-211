# -*- coding: utf-8 -*-
import datetime
import re

from rest_framework import (
    filters,
    mixins,
    permissions,
    serializers,
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from django.db.models import Q, Count, BooleanField
from django.db.models.functions import Cast
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from notifications.models import (
    UserDevice,
    UserNotification,
    Notification,
    Topic,
)
from notifications.push.settings import SETTINGS

from .permissions import IsOwner
from .filters import UserNotificationsFilter
from .serializers import (
    DeviceSerializer,
    TopicSerializer,
    UserNotificationSerializer,
    NotificationSerializer,
)


class UserNotificationViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = UserNotification.objects.all()

    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    serializer_class = UserNotificationSerializer

    filter_backends = (filters.SearchFilter, UserNotificationsFilter)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class NotificationViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.all()

    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)

    serializer_class = NotificationSerializer


# Mixins
class DeviceViewSetMixin:
    lookup_field = "device_id"

    def create(self, request, *args, **kwargs):
        serializer = None
        is_update = False
        if (
            SETTINGS.get("UPDATE_ON_DUPLICATE_REG_ID")
            and "registration_id" in request.data
        ):
            instance = self.queryset.model.objects.filter(
                registration_id=request.data["registration_id"]
            ).first()
            if instance:
                serializer = self.get_serializer(instance, data=request.data)
                is_update = True
        if not serializer:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        if is_update:
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            if SETTINGS["ONE_DEVICE_PER_USER"] and self.request.data.get(
                "active", True
            ):
                UserDevice.objects.filter(
                    user=self.request.user).update(active=False)
            return serializer.save(user=self.request.user)
        return serializer.save()

    def perform_update(self, serializer):
        if self.request.user.is_authenticated:
            if SETTINGS["ONE_DEVICE_PER_USER"] and self.request.data.get(
                "active", False
            ):
                UserDevice.objects.filter(
                    user=self.request.user).update(active=False)

            return serializer.save(user=self.request.user)
        return serializer.save()


class AuthorizedMixin:
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        # filter all devices to only those belonging to the current user
        return self.queryset.filter(user=self.request.user)


# ViewSets
class DeviceViewSet(DeviceViewSetMixin, ModelViewSet):
    queryset = UserDevice.objects.order_by("-id")
    serializer_class = DeviceSerializer

    def get_object(self):
        """
        Returns the device requested by either device_id or registration_id.

        Tries to fetch the device by device_id first, but if it fails
        it will fallback to feth it via registration_id
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        try:
            obj = get_object_or_404(queryset, **filter_kwargs)
        except Http404:
            filter_kwargs = {'registration_id': self.kwargs[lookup_url_kwarg]}
            obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class DeviceCreateOnlyViewSet(DeviceViewSetMixin, CreateModelMixin, GenericViewSet):
    queryset = UserDevice.objects.all()
    serializer_class = DeviceSerializer


class DeviceAuthorizedViewSet(AuthorizedMixin, DeviceViewSet):
    pass


class TopicViewSet(ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = super().get_queryset()
        subscribed = Cast(
            Count('subscribers', filter=Q(subscribers=self.request.user)),
            output_field=BooleanField()
        )
        return qs.annotate(subscribed=subscribed)

    @action(methods=['post'], detail=True)
    def subscribe(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.subscribers.add(request.user)
        setattr(obj, 'subscribed', True)
        data = self.serializer_class(instance=obj).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def unsubscribe(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.subscribers.remove(request.user)
        setattr(obj, 'subscribed', False)
        data = self.serializer_class(instance=obj).data
        return Response(data, status=status.HTTP_201_CREATED)
