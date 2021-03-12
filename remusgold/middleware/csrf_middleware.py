class CSRFMiddleware(object):
    """Middleware for disabling CSRF on d-pog.com"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)

    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return(request)

