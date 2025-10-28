from celery import shared_task
from app.models import Coin
from sqlalchemy import select
from app.core.db import sync_engine
from sqlalchemy.orm import Session

from app.services.bybit import (
    bybit_coin_balance, add_coin_order, get_info_coin)
from asgiref.sync import async_to_sync


PROCENT_SELL = 1.05


@shared_task(name='start_task')
def start_task():
    """
    Осуществляется поиск монет в базе данных у которых стоит
    флаг start=True
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

        balance = async_to_sync(bybit_coin_balance)(coin.user, coin.name)
        balance = balance['balance']

        ticker = async_to_sync(get_info_coin)(coin.user, coin.name)
        print(ticker)
        
        sell_price = round(
            coin.price_buy * PROCENT_SELL, ticker['znak_price'])
        print(sell_price)
        # qwe = async_to_sync(add_coin_order)(
        #     user=coin.user,
        #     symbol=coin.name + 'USDT',
        #     qty=balance,
        #     price=sell_price,
        #     side='Sell'
        # )
        # print(qwe)
 
        return f'Установка ордеров для монеты {coin.name}'

