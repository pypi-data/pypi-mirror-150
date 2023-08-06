import asyncio
import logging
import os
import re
from datetime import datetime
from queue import Empty
from threading import Thread, Event
from time import sleep
from typing import Mapping, AnyStr, Optional

from aiogram import types, Bot, Dispatcher

from .localisation import FormatHandler, TranslateHandler, ServiceVocabulary
from .model.db_model import ServiceModel
from .utils import Singleton, threadsafety_dict

logger = logging.getLogger(os.path.split(__file__)[-1])


class UserSessionException(Exception):
    pass


class CompleteFlowException(UserSessionException):
    pass


def _occur_from_obj(message: types.Message, *items):
    temp_ = message
    for item in items:
        temp_ = getattr(temp_, item)
        assert temp_, f"Cannot occur '{item}' from {temp_}"
    return temp_


def _replace_custom_capture(class_obj, caption: str):
    for pattern in re.findall(r'({[a-z_\.]+})', caption, re.IGNORECASE):
        class_ = pattern[1:-1].split('.')[0]
        if class_obj.__class__.__name__ == class_:
            replacement = _occur_from_obj(class_obj, *pattern[1:-1].split('.')[1:])
            caption = caption.replace(pattern, replacement)
    return caption


def get_prompt(*items, message: Optional[types.Message] = None):
    prompt = ServiceVocabulary.get_path(*items)
    if message:
        prompt = _replace_custom_capture(message, prompt)
    return prompt


class UserSession:
    def __init__(self, user_id, user_name, language='en'):
        self.start_ts = datetime.now()
        self.user_id = user_id
        self.user_name = user_name
        self.language = language
        self._last_item = 0
        self._flow_name = ''
        self._parent_flow_name = None
        logger.info(f"Session for user '{self.user_name}' created")

    def __str__(self):
        return f"{self.__class__.__name__}::{self.user_name} (Started: {self.start_ts.strftime('%H:%M:%S %d-%m-%y')})"

    def get_prompt(self, message: Optional[types.Message] = None):
        return get_prompt('flows', self._flow_name, self._last_item, 'language', self.language, message=message)

    def set_flow(self, name, parent=None):
        self._flow_name = name
        self._parent_flow_name = parent

    def set_item(self, value):
        FormatHandler(ServiceVocabulary.get_path('flows', self._flow_name, self._last_item), value)
        value = TranslateHandler(ServiceVocabulary.get_path('flows', self._flow_name, self._last_item), value)

        setattr(self, ServiceVocabulary.get_path('flows', self._flow_name, self._last_item, 'name'), value)
        logger.info(
            f"{self} -> {ServiceVocabulary.get_path('flows', self._flow_name, self._last_item, 'name')}: {value}")

    def move_to_next(self):
        try:
            self._last_item += 1
            assert self._last_item < len(ServiceVocabulary.get_path('flows', self._flow_name))
        except AssertionError:
            raise CompleteFlowException

    def as_dict(self):
        result = dict(user_id=self.user_id, language=self.language)
        if self.user_name:
            result.update(user_name=self.user_name)
        else:
            result.update(user_name='')
        for item in ServiceVocabulary.get_path('flows', self._flow_name):
            result.update({item['name']: getattr(self, item['name'], None)})
        return result

    def is_expired(self, expire_interval):
        return True if (datetime.now() - self.start_ts).total_seconds() > expire_interval else False


@Singleton
class _OpenSessions(threadsafety_dict, ServiceModel, Mapping[AnyStr, UserSession]):
    def __init__(self):
        threadsafety_dict.__init__(self)
        self._event = None
        self.expire_period = None
        self._timer = None
        self._bot: Bot = None
        self._expired_cache: threadsafety_dict = threadsafety_dict()

    def start(self, **kwargs):
        self._event = kwargs.get('event', None) or Event()
        self.expire_period = float(kwargs.get('expire', None) or 3600)
        self._bot = kwargs.get('bot')
        self._timer = Thread(target=self._run, name='SessionCache', daemon=False)
        self._timer.start()

    def __delitem__(self, key):
        logger.info(f"Clear session: {key}")
        threadsafety_dict.__delitem__(self, key)

    def __setitem__(self, key, value):
        logger.info(f"Initiate session: {key}")
        try:
            del self.expired_cache[key]
            logger.debug(f"User ({key}) session restarted")
        except KeyError:
            logger.debug(f"User ({key}) new session initiated")
        finally:
            threadsafety_dict.__setitem__(self, key, value)

    def __getitem__(self, key) -> UserSession:
        logger.info(f"Get session: {key}")
        return threadsafety_dict.__getitem__(self, key)

    @property
    def expire_period(self):
        return self._expire_period

    @expire_period.setter
    def expire_period(self, value: float):
        self._expire_period = value

    @property
    def expired_cache(self) -> threadsafety_dict:
        return self._expired_cache

    def is_session_expired(self, user_id):
        return user_id in self.expired_cache.keys()

    def _run(self):
        while not self._event.is_set():
            index = list(self.keys())
            for user_id in index:
                session: UserSession = self[user_id]
                if session.is_expired(self._expire_period):
                    try:
                        logger.info(f"Session for user {session.user_name} expired")
                        self.expired_cache[user_id] = session
                    except Exception as e:
                        logger.error(f"Cannot notify user '{session.user_name} ({user_id})'; "
                                     f"Error: {type(e).__name__}:{e}")
                    finally:
                        del self[user_id]
            sleep(2)

    def join(self, timeout: Optional[float] = None):
        self._event.set()
        self._timer.join(timeout)


OpenSessions: _OpenSessions = _OpenSessions()


async def background_expired_sessions_handler(dispatcher: Dispatcher):
    """background task which is created when bot starts"""

    logger.debug(f"Start expired sessions monitoring")
    while True:
        try:
            user_id, item = OpenSessions.expired_cache.get()
            try:
                logger.info(f"Expired item: {item}")
                await dispatcher.bot.send_message(user_id, f"Session for user {item.user_alias} expired")
            except Exception as e:
                logger.error(f"Cannot notify user: {item.user_alias}; Error: {e}")
        except Empty:
            if OpenSessions.event.is_set():
                logger.debug(f"Stop expired sessions monitoring")
                break
        await asyncio.sleep(5)


__all__ = [
    'OpenSessions',
    'UserSession',
    'get_prompt',
    'background_expired_sessions_handler',
    'CompleteFlowException'
]

# if __name__ == '__main__':
#     from localisation import ServiceVocabulary
#     from google_sheets import DB
#     OpenSessions.start()
#     ServiceVocabulary.load()
#
#     class Message:
#         pass
#
#     class User:
#         pass
#
#     user = User()
#     setattr(user, 'full_name', 'Dima')
#     msg = Message()
#     setattr(msg, 'from_user', user)
#
#     get_prompt('flows', 'cancel', 0, 'language', 'ru', message=msg)
#     try:
#         _id = '743554608'
#         OpenSessions[_id] = UserSession(_id, None, 'ru')
#         # OpenSessions[_id].set_flow('Registration', ServiceVocabulary.get('flows', {}).get('register', {}))
#         OpenSessions[_id].set_flow('register') #), ServiceVocabulary.get('flows', {}).get('register', {}))
#         print(f"{OpenSessions[_id].get_prompt(msg)}")
#         OpenSessions[_id].set_item('Кандидат')
#         OpenSessions[_id].move_to_next()
#         print(f"{OpenSessions[_id].get_prompt()}")
#         OpenSessions[_id].set_item('Дима')
#         OpenSessions[_id].move_to_next()
#
#         # sleep(10)
#         # item = OpenSessions.expired_cache.get()
#         # print(f"{item}")
#
#         print(f"{OpenSessions[_id].get_prompt()}")
#         OpenSessions[_id].set_item('Ог')
#         OpenSessions[_id].move_to_next()
#         print(f"{OpenSessions[_id].get_prompt()}")
#         OpenSessions[_id].set_item('doguz@mail.ru')
#         OpenSessions[_id].move_to_next()
#         print(f"{OpenSessions[_id].get_prompt()}")
#         OpenSessions[_id].set_item('0528545803')
#         OpenSessions[_id].move_to_next()
#         OpenSessions[_id].set_item('Stam text')
#         OpenSessions[_id].move_to_next()
#     except UserSessionException as e:
#         if isinstance(e, CompleteFlowException):
#             res = OpenSessions[_id].as_dict()
#             print(f"{res}")
#             DB.set_person(**res)
#         else:
#             raise
#     except Exception as e:
#         print(f"Error: {e}")
