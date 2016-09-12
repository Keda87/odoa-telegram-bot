import logging
from odoa import ODOA
from unqlite import UnQLite

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
odoa = ODOA()
OWNER_ID = None  # Set your telegram ID if you want this bot send you error log.
unqlite = UnQLite('odoa')


def get_surah():
    surah = odoa.get_random_surah()
    message = '{desc}\n\n{ayat}\n{translate}'.format(
        desc=surah.desc,
        ayat=surah.ayah,
        translate=surah.translate
    )
    return message


def subscribe(bot, update):
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    if telegram_id not in unqlite:
        unqlite[telegram_id] = {
            'username': username,
            'first_name': update.message.from_user.first_name,
            'last_name': update.message.from_user.last_name,
            'message': update.message.text
        }
        message = 'Hi {name}, thank you for subscribing SaHaDa updates.'.format(
            name=username
        )
        logger.info('User subscribed: {chat_id}'.format(
            chat_id=update.message.chat_id)
        )
    else:
        message = 'Hi {name}, your telegram ID already registered.'.format(
            name=username
        )
        logger.info('User {username} already subscribed.'.format(
            username=username)
        )
    bot.sendMessage(chat_id=telegram_id, text=message)


def unsubscribe(bot, update):
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    try:
        del unqlite[telegram_id]
        message = 'Hi {name}, your account removed from SaHaDa subscription.'.format(
            name=username
        )
    except:
        message = 'Hi, {name}, your account not registered yet.'.format(
            name=username
        )
        logger.info('User unsubscribed: {chat_id}'.format(
            chat_id=update.message.chat_id)
        )
    bot.sendMessage(chat_id=telegram_id, text=message)


def random(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text=get_surah())


def start(bot, update):
    chat_id = update.message.chat_id
    message = ('Welcome to SaHaDa (Satu Hari Dua Ayat) and thanks for using '
               '@NgajiBot, any question? just ask my creator @adiyatmubarak')
    bot.sendMessage(chat_id=chat_id, text=message)


def surah_sender(bot=None):
    for s in unqlite:
        try:
            bot.sendMessage(chat_id=s[0], text=get_surah())
        except Exception:
            logger.info('An error sending to {id}'.format(id=s['telegram_id']))
        else:
            logger.info('Success send surah to {id}'.format(id=s['telegram_id']))


def get_bot_config():
    import telegram
    from ConfigParser import RawConfigParser
    config = RawConfigParser()
    config.read('config.ini')
    bot = telegram.Bot(token=config.get('main', 'token'))
    return bot


def broadcast(message=None):
    if message:
        bot = get_bot_config()
        for s in unqlite:
            try:
                bot.sendMessage(chat_id=s[0], text=message)
            except Exception:
                logger.info(
                    'An error sending to {id}'.format(id=s['telegram_id']))
            else:
                logger.info(
                    'Success send broadcast to {id}'.format(id=s['telegram_id'])
                )


def manual_send_surah():
    bot = get_bot_config()
    surah_sender(bot)    


def error(bot, update, error):
    message = 'Update %s caused error %s' % (update, error)
    logger.warn(message)
    # Send error log directly to the bot creator if the owner ID filled.
    if OWNER_ID is not None:
        bot.sendMessage(chat_id=OWNER_ID, text=message)
