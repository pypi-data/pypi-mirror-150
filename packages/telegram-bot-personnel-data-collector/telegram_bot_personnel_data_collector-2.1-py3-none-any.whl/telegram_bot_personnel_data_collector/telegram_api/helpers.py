import logging
import os

from aiogram import types

from telegram_bot_personnel_data_collector.configurations import Configurations
from telegram_bot_personnel_data_collector.google_sheets import DB_AS_GoogleSheet
from telegram_bot_personnel_data_collector.session_cache import get_prompt
from telegram_bot_personnel_data_collector.utils import get_error_info
from .service import Service

logger = logging.getLogger(os.path.split(__file__)[-1])


async def update_admins(**update_info):
    for admin_user in DB_AS_GoogleSheet.get_persons(user_id=Configurations.get_admin_list):
        try:
            user_name = update_info.get('user_name', '')
            if user_name is None or user_name == '':
                user_name = update_info.get('contact_email')
                update_info.update(user_name=user_name)
            msg = get_prompt('admin_message', 'text', admin_user.get('language'))
            await Service.bot.send_message(admin_user.get('user_id'),
                                           msg.format(admin=admin_user.get('first_name'), **update_info),
                                           parse_mode='html')
        except Exception as e:
            f, l = get_error_info()
            logger.error(f"Cannot send message to admin: {admin_user}\nError: {e}; File: {f}:{l}")


def is_admin(message: types.Message, *admin_list) -> bool:
    logger.info(f"Admin list: {admin_list}\n\t\tCurrent user: {message.from_user}")
    try:
        assert str(message.from_user.id) in [str(user.get('user_id')) for user in admin_list]
    except AssertionError:
        return False
    else:
        return True


__all__ = [
    'update_admins',
    'is_admin'
]
