from celery.schedules import crontab

BROKER_URL = 'redis://localhost'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERYBEAT_SCHEDULE = {
    'odoa-scheduler': {
        'task': 'tasks.broadcast_surah',
        'schedule': crontab(hour=6, minute=30)  # Execute every 6.30 AM
    }
}
