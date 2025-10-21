from celery import Celery
from celery.schedules import crontab
from app.core.config import settings


CELERY_HOST = 'localhost' if settings.DEBUG else 'redis_service'
BROKER = f'redis://:{settings.redis_pass}@{CELERY_HOST}:6380/0'
celery_app = Celery("Селери", broker=BROKER, backend=BROKER)
celery_app.autodiscover_tasks([
    "app.tasks",       # ищет все задачии в папке app/tasks
])

# Настройка периодического выполнения задач
celery_app.conf.beat_schedule = {
    "say_hello_every_minute": {  # уникальное имя задачи в расписании
        "task": "app.tasks.say_hello",  # полное имя задачи
        "schedule": crontab(minute="*"),  # каждый 1-й интервал минуты
        "args": (),                     # аргументы для задачи
    }
}

celery_app.conf.timezone = "Europe/Moscow"
celery_app.conf.enable_utc = False  # важно отключить UTC
