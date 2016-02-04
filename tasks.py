import logging

import telegram
from odoa import ODOA


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
logger = logging.getLogger(__name__)

# Initialize surah generator.
odoa = ODOA()

def get_surah():
    surah = odoa.get_random_surah()
    message = '{}\n{}'.format(surah.get('ayat'), surah.get('translate'))
    return message

def subscribe(bot, update):
    logger.info('User subscribed: %d' % update.message.chat_id)

def unsubscribe(bot, update):
    logger.info('User unsubscribed: %d' % update.message.chat_id)

def random(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text=get_surah())

def surah_sender(bot):
    bot.sendMessage(chat_id='86274920', text=get_surah())

def error(bot, update, error):
    logger.warn('Update %s caused error %s' % (update, error))
