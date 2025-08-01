from django.http import HttpResponseForbidden

ALLOWED_REFERERS = [
    "https://dronegasm.vercel.app",
]

class RestrictRefererMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        referer = request.META.get('HTTP_REFERER', '')
        origin = request.META.get('HTTP_ORIGIN', '')

        if referer.startswith(tuple(ALLOWED_REFERERS)) or origin.startswith(tuple(ALLOWED_REFERERS)):
            return self.get_response(request)
        return HttpResponseForbidden("Access Denied")
