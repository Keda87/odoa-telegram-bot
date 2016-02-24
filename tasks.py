import logging
from odoa import ODOA
from models import Subscriber


logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
logger = logging.getLogger(__name__)
odoa = ODOA()


def get_surah():
    surah = odoa.get_random_surah()
    message = '{ayat}\n{translate}'.format(ayat=surah.get('ayat'),
                                           translate=surah.get('translate'))
    return message


def subscribe(bot, update):
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    instance = Subscriber.findone(telegram_id=telegram_id)
    if instance not in Subscriber:
        meta = {
            'telegram_id': telegram_id,
            'username': username,
            'first_name': update.message.from_user.first_name,
            'last_name': update.message.from_user.last_name,
            'message': update.message.text
        }
        user = Subscriber(**meta)
        user.save()
        message = 'Hi {name}, thank you for subscribing ODOA updates.'.format(name=username)
        logger.info('User subscribed: {chat_id}'.format(chat_id=update.message.chat_id))
    else:
        message = 'Hi {name}, your telegram ID already registered.'.format(name=username)
        logger.info('User {username} already subscribed.'.format(username=username))

    bot.sendMessage(chat_id=telegram_id, text=message)


def unsubscribe(bot, update):
    telegram_id = update.message.from_user.id
    username = update.message.from_user.username
    instance = Subscriber.findone(telegram_id=telegram_id)
    if instance in Subscriber:
        instance.destroy()
        message = 'Hi {name}, your account removed from ODOA subscription.'.format(name=username)
    else:
        message = 'Hi, {name}, your account not registered yet.'.format(name=username)
        logger.info('User unsubscribed: {chat_id}'.format(chat_id=update.message.chat_id))

    bot.sendMessage(chat_id=telegram_id, text=message)


def random(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text=get_surah())


def surah_sender(bot):
    subs = Subscriber.select(Subscriber.telegram_id).execute()
    for s in subs.all():
        bot.sendMessage(chat_id=s['telegram_id'], text=get_surah())


def error(bot, update, error):
    logger.warn('Update %s caused error %s' % (update, error))
