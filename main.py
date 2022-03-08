import asyncio
import logging.config
from signal import SIGINT, SIGTERM, SIGHUP

from price_generator import PriceGenerator
from settings import settings
from common_logging import utils


if __name__ == '__main__':
    logging.config.dictConfig(utils.get_logger(log_level=settings.LOGLEVEL))
    price_generator = PriceGenerator(ticker_count=settings.TICKERS_COUNT)

    loop = asyncio.new_event_loop()
    loop.create_task(price_generator.serve_generator())

    def _cancel():
        if price_generator.is_running():
            price_generator.stop()

        loop.remove_signal_handler(SIGINT)
        loop.remove_signal_handler(SIGTERM)
        loop.remove_signal_handler(SIGHUP)

    loop.add_signal_handler(SIGINT, _cancel)
    loop.add_signal_handler(SIGTERM, _cancel)
    loop.add_signal_handler(SIGHUP, _cancel)

    try:
        loop.run_forever()  # TODO: fix stop loop
    except (KeyboardInterrupt, asyncio.CancelledError):
        _cancel()
    finally:
        if loop.is_running():
            loop.stop()
