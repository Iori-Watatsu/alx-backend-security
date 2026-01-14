from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    one_hour_ago = now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    ip_counts = {}
    for log in logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason='High request volume'
            )

    sensitive = logs.filter(path__in=['/admin', '/login'])
    for log in sensitive:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason='Sensitive path access'
        )
        