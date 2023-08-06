import asyncio
import logging
import os
from typing import Callable, Optional

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import NetworkError

from ..model.db_model import ServiceModel
from ..utils import Singleton

logger = logging.getLogger(os.path.split(__file__)[-1])


@Singleton
class _service(ServiceModel):
    network_retry = 10
    counter = 0

    def __init__(self, token):
        self._token = token
        self._bot: Optional[Bot] = None
        self._dp = None
        self._on_startup = None
        self.skip_updates = True

    def set_on_startup(self, callback: Callable):
        self._on_startup = callback

    @property
    def bot(self):
        if not self._bot:
            self._bot = Bot(token=self._token)
        return self._bot

    @property
    def dp(self):
        if not self._dp:
            self._dp = Dispatcher(self.bot)
        return self._dp

    # @staticmethod
    # def register_on_startup(*callbacks):
    #     for callback in callbacks:
    #         try:
    #             asyncio.create_task(callback)
    #             logger.info(f"Callback '{callback.__name__}' registered")
    #         except Exception as e:
    #             logger.error(f"Callback '{callback.__name__}' register error: {e}")
    #     logger.info("Bot started online service")

    def start(self, **kwargs):
        while True:
            try:
                # self.register_on_startup(*kwargs.get('start_up', []))
                executor.start_polling(self.dp, skip_updates=self.skip_updates, on_startup=kwargs.get('start_up', []))
            except NetworkError as e:
                if self.counter > self.network_retry:
                    raise
                logging.warning(f"Cannot restart service for {self.counter} times; {e}")
                self.counter += 1
            except Exception as e:
                logger.error(f"Start error: {e}")
            finally:
                pass

    def stop(self):
        self.dp.stop_polling()


Service: _service = _service(os.getenv('TOKEN'))


__all__ = [
    'Service'
]
