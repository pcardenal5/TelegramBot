from src.LogService import LogService
from src.WebToMarkdown import WebToMarkdown

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import dotenv_values


API_KEY = dotenv_values().get('API_KEY')
if API_KEY is None:
    raise LookupError('Could not find API_KEY in .env file!')


logger = LogService().log
wtm = WebToMarkdown(logs = logger)

async def commandStart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if update.message is not None and user is not None:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True)
        )


async def commandHelp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    if update.message is not None:
        reply = '''Los comandos disponibles son los siguientes :
        - /start
        - /help
        - /downloadUrl
        '''.replace('    ','')

        await update.message.reply_text(reply,reply_markup=ForceReply(selective=True))


async def commandDownloadUrl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Descargar la página web proporcionada por el usuario"""
        
    if update.message is None or update.message.text is None:
        return

    file = wtm.downloadUrl(update.message.text.replace('/downloadUrl', ''))
    if file is None:
        await update.message.reply_text('Error procesando la página web solicitada')
        return

    with open(file, 'rb') as outputFile:
        await update.message.reply_document(outputFile)


application = Application.builder().token(API_KEY).build()

# Añadir comandos
application.add_handler(CommandHandler("start", commandStart))
application.add_handler(CommandHandler("help", commandHelp))
application.add_handler(CommandHandler("downloadUrl", commandDownloadUrl))


# Run the bot until the user presses Ctrl-C
application.run_polling(allowed_updates=Update.ALL_TYPES)
