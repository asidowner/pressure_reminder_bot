import logging
import os
import datetime
import pytz

from pd_bot.sql.sql_driven import DBConnection
from pd_bot.plot.pressure_plot import get_plot
from pd_bot.formatter.pressure_as_str import pressure_as_str
from pd_bot.config import PLOT_DIR_NAME
from logging import Logger

from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import dispatcher
from telegram.ext import jobqueue
from telegram.ext import MessageHandler
from telegram.ext import Filters


class BotDriven:
    def __init__(self):
        self.updater = Updater(token=os.environ['PD_BOT_TOKEN'], use_context=True)
        self.dispatcher: dispatcher = self.updater.dispatcher
        self.sql_driven: DBConnection = DBConnection()
        self.logger: Logger = logging.getLogger()
        self.allowed_chat_id = os.environ['PD_BOT_ALLOWED_CHAT_ID']
        self.job: jobqueue = self.updater.job_queue
        self._append_handler()

    def save_pressure(self, update: Update, context: CallbackContext) -> None:
        chat_id: int = update.effective_chat.id
        if not self.bot_allowed(chat_id):
            return
        if len(context.args) != 3:
            self.logger.info('Save pressure. Args on call != 3')
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, Expected 3 params,"
                                                                            " systolic_pressure,"
                                                                            " diastolic_pressure, pulse")
            return
        try:
            systolic_pressure: int = int(context.args[0])
            diastolic_pressure: int = int(context.args[1])
            pulse: int = int(context.args[2])
        except Exception as e:
            self.logger.error(e)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, support only digits")
            return

        self.sql_driven.insert_pressure_data(chat_id=chat_id,
                                             systolic_pressure=systolic_pressure,
                                             diastolic_pressure=diastolic_pressure,
                                             pulse=pulse)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Pressure data saved")

    def get_plot(self, update: Update, context: CallbackContext) -> None:
        chat_id: int = update.effective_chat.id
        if not self.bot_allowed(chat_id):
            return
        pressure_data = self.sql_driven.select_pressure_data()
        plot_file_path: str = os.path.join(PLOT_DIR_NAME, f'plot_{datetime.datetime.now()}.png')
        plot: bytes = get_plot(chat_id=chat_id, pressure_data=pressure_data, file_name=plot_file_path)
        context.bot.send_document(chat_id, document=plot)

    def get_pressure_data_as_str(self, update: Update, context: CallbackContext) -> None:
        chat_id: int = update.effective_chat.id
        if not self.bot_allowed(chat_id):
            return
        pressure_data = self.sql_driven.select_pressure_data()
        context.bot.send_message(chat_id=update.effective_chat.id, text=pressure_as_str(chat_id, pressure_data))

    def get_send_remind(self, update: Update = None, context: CallbackContext = None):
        self.dispatcher.bot.send_message(chat_id=self.allowed_chat_id, text="Save your pressure. use /save_pressure")

    @staticmethod
    def unknown(update: Update, context: CallbackContext) -> None:
        help_text = """Sorry, I didn't understand that command. try to use:
/save {systolic_pressure} {diastolic_pressure} {pulse} for save pressure data
/plot to get plot with pressure data
/data to get pressure data by text"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

    def callback_auto_message(self, context: CallbackContext) -> None:
        context.bot.send_message(chat_id=self.allowed_chat_id, text='Save your pressure data')

    def bot_allowed(self, chat_id: int) -> bool:
        if str(chat_id) != self.allowed_chat_id:
            self.logger.info('Not allowed')
            return False
        else:
            return True

    def start_auto_messaging(self, update: Update, context: CallbackContext) -> None:
        chat_id: int = update.message.chat_id
        if not self.bot_allowed(chat_id):
            return
        context.job_queue.run_daily(self.callback_auto_message,
                                    time=datetime.time(hour=10, minute=0, tzinfo=pytz.timezone('Europe/Moscow')),
                                    days=(0, 1, 2, 3, 4, 5, 6),
                                    context=chat_id)
        context.job_queue.run_daily(self.callback_auto_message,
                                    time=datetime.time(hour=15, minute=0, tzinfo=pytz.timezone('Europe/Moscow')),
                                    days=(0, 1, 2, 3, 4, 5, 6),
                                    context=chat_id)
        context.job_queue.run_daily(self.callback_auto_message,
                                    time=datetime.time(hour=20, minute=0, tzinfo=pytz.timezone('Europe/Moscow')),
                                    days=(0, 1, 2, 3, 4, 5, 6),
                                    context=chat_id)

    def stop_notify(self, update, context):
        chat_id = update.message.chat_id
        if not self.bot_allowed(chat_id):
            return
        context.bot.send_message(chat_id=chat_id, text='Stopping automatic messages!')
        jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        for job in jobs:
            job.schedule_removal()

    def _append_handler(self):
        self.dispatcher.add_handler(CommandHandler('save', self.save_pressure))
        self.dispatcher.add_handler(CommandHandler('plot', self.get_plot))
        self.dispatcher.add_handler(CommandHandler('data', self.get_pressure_data_as_str))
        self.dispatcher.add_handler(CommandHandler("auto", self.start_auto_messaging))
        self.dispatcher.add_handler(CommandHandler("stop", self.stop_notify))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.unknown))
        self.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

    def run_bot(self):
        self.updater.start_polling()
        self.updater.idle()
