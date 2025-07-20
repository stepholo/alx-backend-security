from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_suspicious_ips():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)

    # Flag IPs exceeding 100 requests/hour
    ip_counts = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(count=models.Count('id'))
        .filter(count__gt=100)
    )
    for entry in ip_counts:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': 'High request rate (>100/hour)'}
        )

    # Flag IPs accessing sensitive paths
    logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=SENSITIVE_PATHS
    ).values_list('ip_address', flat=True).distinct()
    for ip in logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults={'reason': 'Accessed sensitive path'}
        )