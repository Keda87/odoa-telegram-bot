import logging
import os

from dotenv import load_dotenv, find_dotenv
from odoa import ODOA
from telegram.ext import Updater, CommandHandler

from dbutils import DBUtils

odoa = ODOA()
load_dotenv(find_dotenv())
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
db = DBUtils(db_name=os.getenv('DB'))


def get_surah():
    surah = odoa.get_random_surah()
    ayah = surah.ayah.decode('utf8')
    description = surah.desc
    translate = surah.translate
    message = f'{description}\n\n{ayah}\n\n{translate}'
    return message


def start_handler(bot, update):
    username = update.message.from_user.username
    message = (f'Hi {username},\n\n'
               f'SaHaDa akan mengirimkan 2 surat beserta terjemahan setiap '
               f'harinya tanpa biaya apapun.\n\n'
               f'Ketik /subscribe untuk berlangganan dan /unsubscribe '
               f'untuk berhenti berlangganan.\n\n'
               f'Ketik /help untuk bantuan.')
    update.message.reply_text(message)


def help_handler(bot, update):
    help_text = ('/subscribe : Memulai langganan.\n'
                 '/unsubscribe : Berhenti langganan.\n'
                 '/random: Kirim surat secara acak.\n'
                 '/help : Bantuan.')
    update.message.reply_text(help_text)


def publish_handler(bot, update):
    message = get_surah()
    for x in db.fetch_all():
        telegram_id = x.get('telegram_id')
        try:
            bot.sendMessage(chat_id=telegram_id, text=message)
        except Exception:
            logger.error(f'Failed send surah to {telegram_id}')
        else:
            logger.info(f'Send surah to {telegram_id} succeed.')


def subscribe_handler(bot, update):
    telegram_user = update.message.from_user
    username = telegram_user.username

    meta = {
        'telegram_id': telegram_user.id,
        'username': username,
        'first_name': telegram_user.first_name,
        'last_name': telegram_user.last_name,
    }
    is_success = db.insert(**meta)
    if is_success:
        message = (f'Hi {username},\n\n'
                   f'Akun anda telah terdaftar pada daftar langganan SaHaDa.\n\n'
                   f'Apabila anda ingin berhenti berlangganan, cukup kirimkan '
                   f'pesan /unsubscribe')
    else:
        message = f'Hi {username},\n\nAkun anda telah didaftarkan sebelumnya.'
    update.message.reply_text(message)


def unsubscribe_handler(bot, update):
    telegram_user = update.message.from_user
    username = telegram_user.username
    db.delete(telegram_id=telegram_user.id)
    message = (f'Hi {username},\n\n'
               f'Akun anda telah dihapus dari daftar langganan SaHaDa.\n\n'
               f'Kritik dan saran bisa disampaikan ke @adiyatmubarak')
    update.message.reply_text(message)


def random_handler(bot, update):
    message = get_surah()
    update.message.reply_text(message)


def error_handler(bot, update, error):
    """Log Errors caused by Updates."""
    message = 'Update "%s" caused error "%s"', update, error
    owner = os.getenv('OWNER_ID')
    if owner:
        bot.sendMessage(chat_id=owner, text=message)
    logger.warning(message)


def main():
    logger.info('Bot started..')

    updater = Updater(os.getenv('TELEGRAM_TOKEN'))
    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CommandHandler('subscribe', subscribe_handler))
    updater.dispatcher.add_handler(CommandHandler('unsubscribe', unsubscribe_handler))
    updater.dispatcher.add_handler(CommandHandler('random', random_handler))
    updater.dispatcher.add_error_handler(error_handler)

    # Register job scheduler in every 12 hours.
    hours12 = 60 * 60 * 12
    updater.job_queue.run_repeating(publish_handler, hours12)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
