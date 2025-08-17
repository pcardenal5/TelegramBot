from src.LogService import LogService
from src.WebToMarkdown import WebToMarkdown
from src.YoutubeDownloader import YoutubeDownloader

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import dotenv_values


API_KEY = dotenv_values().get('API_KEY')
if API_KEY is None:
    raise LookupError('Could not find API_KEY in .env file!')


logger = LogService().log
wtm = WebToMarkdown(logs = logger)
ytd = YoutubeDownloader(logs = logger)

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
        - /downloadUrl <URL a descargar>
        - /downloadYoutube <URL a descargar>
        '''.replace('    ','')

        await update.message.reply_text(reply,reply_markup=ForceReply(selective=True))


async def commandDownloadWebpage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Descargar la página web proporcionada por el usuario"""

    if (
        update.message is None 
        or update.message.text is None
        or context.args is None
        or len(context.args) != 1
        ):
        return


    file = wtm.downloadUrl(context.args[0])
    if file is None:
        await update.message.reply_text('Error procesando la página web solicitada')
        return

    with open(file, 'rb') as outputFile:
        await update.message.reply_document(outputFile)


async def commandDownloadYoutubeVideo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Descargar la página web proporcionada por el usuario"""
        
    if (
        update.message is None 
        or update.message.text is None
        or context.args is None
        or len(context.args) != 1
        ):
        return


    url = context.args[0]

    await update.message.reply_text(f'Petición recibida, comienza la descarga de {url}...')
    file = ytd.downloadYoutubeVideo(url)
    if file is None:
        await update.message.reply_text('Error procesando la página web solicitada')
        return

    await update.message.reply_text(f'Se ha guardado el vídeo en la ruta {file}')


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        # Los comandos deben ser todos en minúsculas
        ('start',           'Empieza la conversación con el bot'),
        ('help',            'Despliega mensaje de ayuda'),
        ('downloadurl',     'Descarga la página web proporcionada en md.'),
        ('downloadyoutube', 'Descarga el audio del vídeo proporcionado.')
    ])



application = Application.builder().token(API_KEY).post_init(post_init).build()

# Añadir comandos
application.add_handler(CommandHandler("start", commandStart))
application.add_handler(CommandHandler("help", commandHelp))
application.add_handler(CommandHandler("downloadUrl", commandDownloadWebpage, has_args = True))
application.add_handler(CommandHandler("downloadYoutube", commandDownloadYoutubeVideo, has_args = True))


# Run the bot until the user presses Ctrl-C
application.run_polling(allowed_updates=Update.ALL_TYPES)
