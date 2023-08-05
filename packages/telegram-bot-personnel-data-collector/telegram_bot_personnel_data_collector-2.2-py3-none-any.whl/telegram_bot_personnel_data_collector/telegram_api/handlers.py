import logging
import os

from aiogram import types, Dispatcher

from telegram_bot_personnel_data_collector.configurations import Configurations
from telegram_bot_personnel_data_collector.google_sheets import DB_AS_GoogleSheet
from telegram_bot_personnel_data_collector.localisation import ServiceVocabulary, TranslateException, FormatException
from telegram_bot_personnel_data_collector.session_cache import OpenSessions, get_prompt, UserSession, \
    CompleteFlowException
from telegram_bot_personnel_data_collector.telegram_api.helpers import update_admins, is_admin
from telegram_bot_personnel_data_collector.telegram_api.service import Service


logger = logging.getLogger(os.path.split(__file__)[-1])


async def cancel_registration(message: types.Message):
    logger.debug(f"cancel_registration -> {message.from_user.full_name}: {message.text}")
    if message.from_user.id in OpenSessions.keys():
        logger.info(f"Restart session for {message.from_user.id}")
        del OpenSessions[message.from_user.id]
        await message.reply(get_prompt('flows', 'cancel', 0, 'language', message.from_user.language_code,
                                       message=message), parse_mode='html')
    else:
        await message.reply("Registration wasn't started yet", parse_mode='html')


async def register_handler(message: types.Message):
    logger.debug(f"register_handler -> {message.from_user.full_name}: {message.text}")
    if message.from_user.id in OpenSessions.keys():
        logger.info(f"Restart session for {message.from_user.id}")
        await Service.bot.send_message(message.from_user.id, "Session restarted")
        del OpenSessions[message.from_user.id]
    logger.info(f'New user -> {message.from_user.id}: {message.from_user.language_code}')
    user_name = message.from_user.username if message.from_user.username else ''
    OpenSessions[message.from_user.id] = UserSession(message.from_user.id, user_name,
                                                     message.from_user.language_code)
    OpenSessions[message.from_user.id].set_flow('register')
    await message.reply(OpenSessions[message.from_user.id].get_prompt(message), parse_mode='html')


async def role_handler(message: types.Message):
    logger.debug(f"role_handler -> {message.from_user.full_name}: {message.text}")
    if message.from_user.id in OpenSessions.keys():
        command = message.get_command(True)
        OpenSessions[message.from_user.id].set_item(command)
        OpenSessions[message.from_user.id].move_to_next()
        await message.answer(OpenSessions[message.from_user.id].get_prompt(message))
    else:
        await message.reply("Registration wasn't started yet", parse_mode='html')


async def all_handler(message: types.Message):
    logger.debug(f"all_handler -> {message.from_user.full_name}: {message.text}")
    if message.from_user.is_bot:
        await message.reply("Please enter from Group")
        return
    user_id = message.from_user.id
    if user_id not in OpenSessions.keys():
        prompt = "{}".format(ServiceVocabulary.get_path('welcome_banner', 'text', message.from_user.language_code))

        welcome_picture = ServiceVocabulary.get_picture('welcome_banner', 'picture')
        if welcome_picture:
            with open(welcome_picture, 'rb') as photo_stream:
                await Service.bot.send_photo(message.chat.id, photo=photo_stream, caption=prompt, parse_mode='html')
        else:
            await message.answer(prompt, parse_mode='html')
        return
    try:
        OpenSessions[user_id].set_item(f"{message.text}")
        OpenSessions[user_id].move_to_next()
        await message.answer(OpenSessions[user_id].get_prompt(message))
    except CompleteFlowException:
        msg = "User {} registered:\n\t{}".format(
            message.from_user.full_name,
            '\n\t'.join(f"{k}: {v}" for k, v in OpenSessions[message.from_user.id].as_dict().items())
        )
        logger.info(msg)
        result = OpenSessions[message.from_user.id].as_dict()
        DB_AS_GoogleSheet.set_person(**result)
        del OpenSessions[message.from_user.id]
        await message.reply(get_prompt('flows', 'complete', 0, 'language', message.from_user.language_code,
                                       message=message), parse_mode='html')

        await update_admins(**result)
        # for admin in ServiceConfiguration.get('administrators', []):
        #     await Service.bot.send_message(admin.get('id'), f"Thanks, your registration completed\n{msg}")
    except (TranslateException, FormatException) as e:
        await message.reply(f"Wrong data inserted: {e}")
    except Exception as e:
        await message.reply(f"Error: {e}")


async def admin_handler(message: types.Message):
    admin_list = list(DB_AS_GoogleSheet.get_persons(user_id=Configurations.get_admin_list))
    if is_admin(message, *admin_list):
        msg = """Admin permissions granted for you\nFor view all registered persons click <a href="{url}">here</>"""
        await message.answer(msg.format(url=DB_AS_GoogleSheet.table.strip()),
                             parse_mode='html')
    else:
        admin_aliases = [user.get('user_name') for user in admin_list]
        await message.reply(f"Sorry, operation allowed for admins only ({', '.join(admin_aliases)})")


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(register_handler, commands=['register'])
    dp.register_message_handler(role_handler, commands=['Volunteer', 'Candidate'])
    dp.register_message_handler(cancel_registration, commands=['cancel'])
    dp.register_message_handler(admin_handler, commands=['admin'])
    dp.register_message_handler(all_handler)


__all__ = [
    'handlers_register'
]
