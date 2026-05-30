from .base import *  # noqa

# Render handles SSL at the load balancer level, so we must NOT redirect
# (doing so causes infinite redirect loops on Render free tier)
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['https://floodguard-agri.onrender.com'])

# Optional Sentry integration
SENTRY_DSN = env('SENTRY_DSN', default='')
try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration()],
            traces_sample_rate=0.1,
            send_default_pii=False,
        )
except ImportError:
    pass  # sentry_sdk not installed, skipping

