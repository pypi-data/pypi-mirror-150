import os.path, logging
from queue import Queue, Empty
from threading import Thread, RLock, Event
from time import sleep
from typing import Optional

from google_sheets_lib import GoogleSheets

from .utils import Singleton, DBModel

logger = logging.getLogger(os.path.split(__file__)[-1])


@Singleton
class _DB_AS_GoogleSheet(DBModel, Thread):
    def __init__(self):
        Thread.__init__(self, name=self.__class__.__name__, target=self.run)
        self._google_sheet: GoogleSheets = None
        self._sheet_name = ''
        self._work_book = None
        self._table_url = ''
        self._column_map = None

        self._lock = RLock()
        self._event = Event()
        self._queue = Queue()

    def start(self, drive_folder_id=None, logging_level: str = 'INFO', service_account_file: str = None,
              credentials=None, **kwargs):
        self._google_sheet = GoogleSheets(drive_folder_id, logging_level, service_account_file, credentials)
        self._sheet_name = kwargs.get('table_sheet')
        self._table_url = kwargs.get('table_url')
        self._work_book = self._google_sheet.set_sheet(url=self._table_url)
        self._google_sheet.set_ws(title=self._sheet_name)
        logger.info(f"Sheet {self._sheet_name} ready")
        Thread.start(self)

    @property
    def table(self):
        return self._table_url

    @staticmethod
    def filter_person(row, **filters) -> bool:
        for col, look_up in filters.items():
            if row.get(col, None) not in [str(i) for i in look_up]:
                return False
        return True

    def get_persons(self, **kwargs):
        header = self._google_sheet.get_row(1)
        for index in self._google_sheet.get_column(1)[1:]:
            row = self._google_sheet.get_row(int(index) + 1)
            row_dict = {header[cell_id]: value for cell_id, value in enumerate(row)}
            if self.filter_person(row_dict, **kwargs):
                yield row_dict

    def join(self, timeout: Optional[float] = None) -> None:
        if self.is_alive():
            self._event.set()
            Thread.join(self, timeout)
            logger.info(f"Joined normally")
            return
        logger.info("Not stated yet")

    def run(self) -> None:
        logger.info(f"Data monitor of {self.name} started")
        while True:
            try:
                person_properties = self._queue.get()
                logger.debug(f"Dequeued -> Personnel data: {person_properties}")
                self._set_person(**person_properties)
                logger.debug(f"Currently enqueued: {self._queue.qsize()}")
            except Empty:
                logger.debug("Queue empty")
                if self._event.is_set():
                    logger.info(f"Data monitor of {self.name} stopped gracefully")
                    break
                sleep(10)
            except Exception as e:
                logger.error(f"Cannot deque item; Error: {e}")
                raise
            else:
                sleep(1)

    def _set_person(self, **person_properties):
        row_offset = self.is_person_exist(self._google_sheet, **person_properties)
        try:
            self._google_sheet.update_row_by_header([dict(Num=row_offset - 1, **person_properties)], header_row=1,
                                                    row_offset=row_offset)
        except Exception as e:
            logger.error(f"Cannot write person entry: {person_properties}:\n{e}")
            raise

    def set_person(self, **person_properties):
        self._queue.put(person_properties)
        logger.debug(f"Enqueued -> Personnel data: {person_properties}")

    @staticmethod
    def is_person_exist(sheet, **person_properties) -> int:
        last_index = 0
        header = sheet.get_row(1)
        for index, user_id in enumerate(sheet.get_column(header.index('user_id') + 1)):
            last_index = index
            if str(person_properties.get('user_id')) == str(user_id):
                return last_index + 1
        return last_index + 2


DB_AS_GoogleSheet: _DB_AS_GoogleSheet = _DB_AS_GoogleSheet()

__all__ = [
    'DB_AS_GoogleSheet'
]
