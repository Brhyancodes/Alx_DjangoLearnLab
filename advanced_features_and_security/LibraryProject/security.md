# Security checklist (short)

- ENV: Set DJANGO_SECRET_KEY on server.
- DEBUG: Set DJANGO_DEBUG=False in production.
- Cookies: CSRF_COOKIE_SECURE=True and SESSION_COOKIE_SECURE=True only in HTTPS.
- HSTS: set SECURE_HSTS_SECONDS > 0 in production.
- CSP: use django-csp or configure Content-Security-Policy header.
- Forms: always use {% csrf_token %} in templates.
- Views: use @permission_required and Django ORM (no raw string SQL).
- Testing: create test users and check view access per group.
