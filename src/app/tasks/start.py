from celery import shared_task
from app.models import Coin
from sqlalchemy import select
from app.core.db import sync_engine
from sqlalchemy.orm import Session

from app.services.bybit import (
    bybit_coin_balance, add_coin_order, get_info_coin, round_down,
    delete_coin_order
)
from asgiref.sync import async_to_sync
from decimal import Decimal


PROCENT_SELL = 1.05
PROCENT_BUY = 0.95


@shared_task(name='start_task')
def start_task():
    """
    Осуществляется поиск монет в базе данных у которых стоит
    флаг start=True и нет установленных ордеров на покупку или продажу.
    """
    with Session(sync_engine) as session:
        coins = session.scalars(
            select(Coin).where(
                Coin.start.is_(True),
                Coin.order_buy_id.is_(None),
                Coin.order_sell_id.is_(None),
            )
        ).all()
        for coin in coins:
            coin_orders_task.delay(coin.id)
    return "Поиск новых запущеных монет"


@shared_task(name='coin_orders_task')
def coin_orders_task(coin_id: int):
    """Уставнока ордеров для монеты."""
    with Session(sync_engine) as session:
        coin = session.get(Coin, coin_id)
        if not coin:
            return f'Монета с id={coin_id} не найдена'

        # Получвем информацию о монете
        ticker = async_to_sync(get_info_coin)(coin.user, coin.name)

        # Узнаем баланс монеты
        balance_data = async_to_sync(bybit_coin_balance)(coin.user, coin.name)
        balance = Decimal(str(balance_data.get('balance', 0)))
        min_order_qty = Decimal(str(ticker['lotSizeFilter']['minOrderQty']))

        if balance < min_order_qty:
            coin.start = False
            session.commit()
            return (
                f"Недостаточно монет для ордера {coin.name}: "
                f"баланс={balance}, "
                f"минимум={min_order_qty}"
            )
        # Округляем баланс в соответствии с точностью биржи
        balance = round_down(balance, ticker['base_precision'])
        sell_price = round(
            coin.price_buy * PROCENT_SELL, ticker['znak_price'])
        buy_price = round(
            coin.price_buy * PROCENT_BUY, ticker['znak_price'])

        # Удаляем старые ордера если они есть
        async_to_sync(delete_coin_order)(coin.user, coin.name)

        # Создаем новые ордера
        sell_order = async_to_sync(add_coin_order)(
            user=coin.user,
            symbol=coin.name + 'USDT',
            qty=balance,
            price=sell_price,
            side='Sell'
        )
        buy_order = async_to_sync(add_coin_order)(
            user=coin.user,
            symbol=coin.name + 'USDT',
            qty=balance,
            price=buy_price,
            side='Buy'
        )

        # Получаем ID ордеров и сохраняем в базу
        for order in [sell_order, buy_order]:
            if not order:
                continue

            # Извлекаем ключ (Buy/Sell) и значение (ID или ошибка)
            side, value = next(iter(order.items()))

            is_valid_id = value if isinstance(value, int) else None
            if side == 'Buy':
                coin.order_buy_id = is_valid_id
            elif side == 'Sell':
                coin.order_sell_id = is_valid_id

        session.commit()
        return sell_order, buy_order
