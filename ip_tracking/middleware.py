from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
from django_ip_geolocation import IpGeolocationAPI
from django.core.cache import cache
from os import getenv

GEO_API_KEY = getenv('GEO_API_KEY')
geo_api = IpGeolocationAPI(GEO_API_KEY)

class RequestLoggingMiddleware:
    """Middleware to log requests with IP addresses"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.path
        timestamp = timezone.now()

        # Check if the IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exitsts():
            # If the IP is blocked, return a forbidden response
            return HttpResponseForbidden("Your IP address has been blocked.")

        # Geolocaion caching
        cache_key = f"geo_{ip_address}"
        geo_data = cache.get(cache_key)
        if not geo_data:
            response = geo_api.get_geolocation(ip_address)
            geo_data = {
                'country': response.get('country_name', ''),
                'city': response.get('city', '')
            }
            cache.set(cache_key, geo_data, 60 * 60 * 24)

        # Save the log entry
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            timestamp=timestamp,
            country=geo_data['country'],
            city=geo_data['city']
        )
        response = self.get_response(request)
        return response