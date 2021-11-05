from django.utils import timezone

from deadlines.models import Deadline


def get_active_modules(request):
    dt_now = timezone.now()
    queryset = Deadline.objects.all()
    if not request.user.is_superuser:
        queryset = queryset.filter(start_dt__lte=dt_now, end_dt__gte=dt_now)
    return queryset.values()


