import logging
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, InlineQueryHandler, \
    ConversationHandler

from download_video import DownLoad_from_Inst

TOKEN = '1207612249:AAEdvcYQEanqvS_cw4lwoXk1XsTiwKEPUW0'
LINK = 1
COMMAND = 1
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

keyboard = [[InlineKeyboardButton("Скачать видео из Инстаграма",
                                  callback_data='Скачать видео из Инстаграма: /dw_video')],
            [InlineKeyboardButton("Скачать фото из Инстаграма",
                                  callback_data='Скачать видео из Инстаграма: /dw_image')],
            ]


def start(update, context):
    update.message.reply_text(
        f'Hi, {update.message.from_user["first_name"]}!',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="{}".format(query.data))


def get_link(update, context):
    update.message.reply_text('Введите ссылку')
    return LINK


def download_video(update, context):
    try:
        url = re.search(
            r"(?P<url>https?://[^\s]+)",
            update.message.text).group("url")
        if re.search(r"(?P<url>https?://[^\s]+)", update.message.text):
            update.message.reply_text('Идет скачивание...')
            dw = DownLoad_from_Inst(url,
                                    update.message.from_user["first_name"],
                                    video=True)
            if dw.get_url_video() == 'Ready':
                update.message.reply_video(video=dw.video_url)
            else:
                update.message.reply_text('Неверная ссылка')
        else:
            update.message.reply_text('Неверная ссылка')
    except Exception:
        update.message.reply_text('Неверная ссылка')
        return 


def download_image(update, context):
    if re.search(r"(?P<url>https?://[^\s]+)", update.message.text):
        update.message.reply_text('Идет скачивание...')
        dw = DownLoad_from_Inst(
            re.search(
                r"(?P<url>https?://[^\s]+)",
                update.message.text).group("url"),
            update.message.from_user["first_name"])
        if dw.get_url_image() == 'Ready':
            update.message.reply_photo(dw.image_url)
        else:
            update.message.reply_text('Неверная ссылка')
    else:
        update.message.reply_text('Неверная ссылка')


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(
        TOKEN,
        use_context=True,
        request_kwargs={
            'read_timeout': 1000,
            'connect_timeout': 1000})

    dp = updater.dispatcher

    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("start", start))

    conv_handler_video = ConversationHandler(
        entry_points=[CommandHandler('dw_video', get_link)],

        states={
            LINK: [MessageHandler(Filters.text, download_video)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    conv_handler_image = ConversationHandler(
        entry_points=[CommandHandler('dw_image', get_link)],

        states={
            LINK: [MessageHandler(Filters.text, download_image)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler_video)
    dp.add_handler(conv_handler_image)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
