from ConfigParser import RawConfigParser
from telegram import Updater
from tasks import surah_sender, subscribe, unsubscribe, random, error, start

config = RawConfigParser()
config.read('config.ini')

if __name__ == '__main__':
    updater = Updater(token=config.get('main', 'token'))

    # Register bot command.
    updater.dispatcher.addTelegramCommandHandler('start', start)
    updater.dispatcher.addTelegramCommandHandler('subscribe', subscribe)
    updater.dispatcher.addTelegramCommandHandler('unsubscribe', unsubscribe)
    updater.dispatcher.addTelegramCommandHandler('random', random)

    # Register job scheduler in every 12 hours.
    hours12 = 60 * 60 * 12
    updater.job_queue.put(surah_sender, hours12, repeat=True)

    # Add error handler.
    updater.dispatcher.addErrorHandler(error)

    # Start the bot.
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    print 'Bot started..'
