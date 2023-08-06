import os
import sys

from telegram_bot_personnel_data_collector import version
from telegram_bot_personnel_data_collector.arg_parse import parse
from telegram_bot_personnel_data_collector.configurations import Configurations
from telegram_bot_personnel_data_collector.google_sheets import DB_AS_GoogleSheet
from telegram_bot_personnel_data_collector.localisation import ServiceVocabulary
from telegram_bot_personnel_data_collector.session_cache import OpenSessions
from telegram_bot_personnel_data_collector.telegram_api import Service, handlers_register
from telegram_bot_personnel_data_collector.utils import create_logger, get_error_info

logger = None


def main(*callback_list):
    try:
        OpenSessions.start(expire=os.getenv('INACTIVITY_TIMEOUT'), bot=Service.bot)
        DB_AS_GoogleSheet.start(table_url=os.getenv('TABLE_URL'),
                                table_sheet=os.getenv('TABLE_SHEET'),
                                drive_folder_id=os.getenv('TABLE_FOLDER', None),
                                service_account_file=os.path.join(os.getenv('CREDENTIALS'), os.getenv('SECRET_FILE')))
        ServiceVocabulary.load(os.path.join(Configurations.Location, 'content', 'localisation.yaml'))
        Configurations.load(os.path.join(Configurations.Location, 'content', 'administrators.yaml'))
        handlers_register(Service.dp)
        Service.start(start_up=callback_list)

    except KeyboardInterrupt:
        logger.info(f"User keyword interrupt")
    except Exception as e:
        f, l = get_error_info()
        logger.error(f"Unexpected: {e}; File: {f}:{l}")
    finally:
        Service.stop()
        DB_AS_GoogleSheet.join()


if __name__ == '__main__':
    arguments = parse(sys.argv[1:])
    if arguments.version:
        print(f"Current version: {version}")
        sys.exit(0)
    Configurations.Location = arguments.configuration
    logger = create_logger('Bot', arguments.debug)
    main()
