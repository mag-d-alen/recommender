import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
User = get_user_model()


def get_recent_users(days_ago=14, ids_only = True):
    delta = datetime.timedelta(days = days_ago)
    now = timezone.now()
    time_delta = now-delta
    # qs = User.objects.filter(Q(date_joined__gte=time_delta) | Q(last_login__gte=time_delta))
    qs = User.objects.all()[:20]
    if ids_only:
        return qs.values_list('id', flat=True)
    return qs