from ipware import get_client_ip
from .models import RequestLog

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path
        )
        return self.get_response(request)
        