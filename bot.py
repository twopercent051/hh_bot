import asyncio
import logging

from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.handlers.echo import register_echo
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc.sheduler import sheduler_jobs
from tgbot.models.db_connector import sql_start, dumper


from create_bot import bot, dp, config, sheduler

logger = logging.getLogger(__name__)
file_log = logging.FileHandler("logger.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    pass


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)
    # sheduler.start()
    # sheduler_jobs()
    sql_start()

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:

        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
