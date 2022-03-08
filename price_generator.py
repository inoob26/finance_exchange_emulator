import asyncio
import logging

from utils import generate_movement, check_price, gen_ticker_name
from db_client import DBClient, TickerData
from datetime import datetime


class PriceGenerator:
    def __init__(self, ticker_count: int, sleep_timeout: float = 1):
        """
        :param ticker_count: how much ticker data generate
        """
        self._timeout = sleep_timeout
        self._tickers = ticker_count
        self._cancel_event = asyncio.Event()
        self._tasks = None
        self._db_client = DBClient()
        self._logger = logging.getLogger(__name__)

    async def gen_price(self, ticker: str):
        price = 0
        while not self._cancel_event.is_set():
            movement = generate_movement()
            price += movement
            price = check_price(price)

            self._logger.debug(f"ticker: {ticker}, movement: {movement}, price {price}")
            data = TickerData(
                created_at=datetime.utcnow(),
                ticker=ticker,
                price=price
            )
            try:
                await self._db_client.insert_one(ticker=data)
            except asyncio.CancelledError as e:
                self._logger.exception(e)
                self._cancel_event.set()
            await asyncio.sleep(self._timeout)

    async def serve_generator(self):
        self._tasks = [
            asyncio.create_task(self.gen_price(gen_ticker_name(num=item)))
            for item in range(self._tickers)
        ]

        await asyncio.gather(*self._tasks)

    def is_running(self):
        return not self._cancel_event.is_set()

    def stop(self):
        self._logger.warning("price generator has been stopped")
        self._cancel_event.set()
