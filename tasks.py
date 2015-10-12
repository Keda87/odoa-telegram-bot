import telegram

from odoa import ODOA
from celery import Celery

app = Celery('tasks')
app.config_from_object('celery_config')


@app.task
def broadcast_surah():

    # Telegram.
    bot = telegram.Bot(token='...')

    # ODOA
    odoa = ODOA()
    result = odoa.get_random_surah()

    if 'ayat' in result and 'translate' in result:
        odoa_message = """
        {surah}
        {translate}
        """.format(surah=result.get('ayat').encode('utf8'),
                   translate=result.get('translate'))

        bot.sendMessage(chat_id='...', text=odoa_message)

