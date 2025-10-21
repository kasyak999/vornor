from celery import shared_task
from app.core.config import settings
from app.core.celery_worker import celery_app


@shared_task(name='Тестовая задача')
def test_task():
    """Отправка уведомления."""
    print('qwe')
    return "ok"


@shared_task(name='Тестовая задача 2')
def test_task2():
    """Отправка уведомления."""
    print('запускается через 5 секунд')
    return "ok"


@celery_app.task(name="app.tasks.say_hello")
def say_hello():
    print("Привет! Задача сработала через Celery Beat.")
