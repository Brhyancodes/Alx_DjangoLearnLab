class ContentSecurityPolicyMiddleware:
    """
    Minimal CSP header. For more control use django-csp.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csp = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:;"
        response.setdefault("Content-Security-Policy", csp)
        return response
