from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'http_request_total',
    'Total HTTP request',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

USER_REGISTRATION = Counter(
    'user_registration_total',
    'Total user registration',
    ['status']
)

EMAIL_VERIFICATIONS = Counter(
    'email_verifications_total',
    'Total email verifications',
    ['status']
)
