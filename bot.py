from telegram import Updater
from tasks import surah_sender, subscribe, unsubscribe, random, error


if __name__ == '__main__':
    updater = Updater(token='85912576:AAHP8ru0nT6mtnk5tco7mnVb9cjVCcXyDZw')

    # Register bot command.
    updater.dispatcher.addTelegramCommandHandler('subscribe', subscribe)
    updater.dispatcher.addTelegramCommandHandler('unsubscribe', unsubscribe)
    updater.dispatcher.addTelegramCommandHandler('random', random)

    # Register job scheduler.
    # updater.job_queue.put(surah_sender, 3, repeat=True)

    # Add error handler.
    updater.dispatcher.addErrorHandler(error)

    # Start the bot.
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    print 'Bot started..'
