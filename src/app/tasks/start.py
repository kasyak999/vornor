from celery import shared_task


@shared_task(name='Тестовая задача')
def test_task():
    """Отправка уведомления."""
    print('qwe')
    return "ok 1"


@shared_task(name='Тестовая задача 2')
def test_task2():
    """Отправка уведомления."""
    print('запускается через 5 секунд')
    return "ok 2"


from app.models import Coin
from sqlalchemy import select
from app.core.db import AsyncSessionLocal
import asyncio
from asgiref.sync import async_to_sync


@shared_task(name='start_task')
def start_task():
    """
    Осуществляется поиск монет в базе данных у которых стоит
    флаг start=True
    """
    print('Добавление новых задач в очередь')
    # tasks.new_task.apply_async()
    
    async def get_coins():
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Coin).where(
                Coin.start == True))
            return result.scalars().all()
        
    # result = asyncio.run(get_coins())  # запускаем async функцию синхронно
    result = async_to_sync(get_coins)()  # запускаем async функцию синхронно
    print(result)



