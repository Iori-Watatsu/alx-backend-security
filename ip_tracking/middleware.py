from ipware import get_client_ip
from .models import RequestLog
from django.core.cache import cache
from django_ipgeolocation import IpGeolocationAPI
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP

geo = IpGeolocationAPI()

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden()

        location = cache.get(ip)
        if not location:
            data = geo.get(ip)
            location = {
                'country': data.get('country'),
                'city': data.get('city')
            }
            cache.set(ip, location, 86400)

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=location['country'],
            city=location['city']
        )
        return self.get_response(request)
