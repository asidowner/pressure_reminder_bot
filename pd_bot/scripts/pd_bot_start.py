#!/usr/bin/env python
import logging
from pd_bot.bot_driven import BotDriven


def run():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    bot = BotDriven()
    bot.run_bot()


if __name__ == '__main__':
    run()
