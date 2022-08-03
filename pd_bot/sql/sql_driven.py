import os.path
import sqlite3
import logging

from sqlite3 import Error, Connection, Cursor
from logging import Logger
from pd_bot.config import DIR_PATH, DB_PATH


class DBConnection:
    def __init__(self):
        self.conn: Connection or None = None
        self.db_name: str = DB_PATH
        self.logger: Logger = logging.getLogger()
        self._create_table()

    def _connect(self):
        try:
            self.conn: Connection = sqlite3.connect(self.db_name)
        except Error as e:
            self.logger.info('Error when try connect to database')
            self.logger.error(e)
            if self.conn:
                self.conn.close()
            raise

    def _disconnect(self):
        if self.conn:
            self.conn.close()

    def _create_table(self):
        try:
            self._connect()
            cursor: Cursor = self.conn.cursor()
            with open(os.path.join(DIR_PATH, 'sql', 'init_db.sql')) as f:
                cursor.executescript(f.read())
            cursor.close()
        except Error as e:
            self.logger.info('Error when try init db')
            self.logger.error(e)
            raise
        finally:
            self._disconnect()

    def insert_pressure_data(self, chat_id: int, systolic_pressure: int, diastolic_pressure: int, pulse: int):
        if not isinstance(systolic_pressure, int) or not isinstance(diastolic_pressure, int) or not isinstance(pulse,
                                                                                                               int):
            raise TypeError('systolic_pressure or diastolic_pressure or pulse should be int')
        try:
            self._connect()
            cursor: Cursor = self.conn.cursor()
            sql_cmd: str = f"""insert into Pressure ("chat_id", "date_", systolic_pressure, diastolic_pressure, pulse)
             values ({chat_id}, Datetime('now'), {systolic_pressure}, {diastolic_pressure}, {pulse});"""
            cursor.executescript(sql_cmd)
            cursor.close()
        except Error as e:
            self.logger.info('Error when try add pressure data')
            self.logger.error(e)
            raise
        finally:
            self._disconnect()

    def select_pressure_data(self):
        try:
            self._connect()
            cursor: Cursor = self.conn.cursor()
            cursor.execute('select * from Pressure')
            return cursor.fetchall()
        except Error as e:
            self.logger.info('Error when try select pressure data')
            self.logger.error(e)
            raise
        finally:
            self._disconnect()
