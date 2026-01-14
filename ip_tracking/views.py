from django.shortcuts import render
from django.http import JsonResponse
from ratelimit.decorators import ratelimit

# Create your views here.
@ratelimit(key='ip', rate='5/m', method='ALL', block=True)
def login_view(request):
    return JsonResponse({'status': 'ok'})
