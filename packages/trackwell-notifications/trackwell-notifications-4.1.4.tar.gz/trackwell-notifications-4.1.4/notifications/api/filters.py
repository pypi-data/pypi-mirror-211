import datetime
import re

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import SAFE_METHODS

from notifications.models import Notification


class UserNotificationsFilter(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.method not in SAFE_METHODS:
            return super().filter_queryset(request, queryset, view)
        qs = queryset.filter(
            Q(user=request.user) &
            Q(notification__notification_type=Notification.TypeChoices.WEB) &
            (Q(next_display__isnull=True) | Q(next_display__lte=datetime.datetime.now())) &
            (Q(notification__expires__isnull=True) | Q(notification__expires__gte=datetime.datetime.now())) &
            (Q(notification__active_from__isnull=True) | Q(
                notification__active_from__lt=datetime.datetime.now()))
        ).exclude(answer=True).select_related('notification', 'user').order_by('timestamp', 'id')
        host = request.headers['host']
        referer = request.headers.get('referer', None)
        if referer is None:
            return qs
        path = referer.split(host)[-1]
        base_path = path.split('?')[0]
        if base_path:
            qs = [
                un for un in qs
                if re.match(un.notification.display_only_if_url_path_matches_regex, base_path) is not None
            ]
        return qs
