from datetime import timedelta

BROKER_URL = 'redis://localhost'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULE = {
    'odoa-scheduler': {
        'task': 'tasks.broadcast_surah',
        'schedule': timedelta(hours=2)
    }
}
