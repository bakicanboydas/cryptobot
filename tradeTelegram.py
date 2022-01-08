import logging
import sys
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Başladık hadi hayırlısı')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Yardım geliyor')


def echo(update, context):
    """Echo the user message."""
    #update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def alis_satis(fiyati,sayisi,mesaji,kari_zarari,kar_zarar_mesaji,toplam_kar_zarari,denetleyen,symbol):
    global fiyat
    fiyat = fiyati
    global sayi
    sayi = sayisi
    global mesaj
    mesaj = mesaji
    global kar_zarar
    kar_zarar = kari_zarari
    global kar_zarar_mesaj
    kar_zarar_mesaj = kar_zarar_mesaji
    global toplam_kar_zarar
    toplam_kar_zarar =  toplam_kar_zarari
    global denetleyici
    denetleyici = denetleyen
    global coin
    coin = symbol
    main()
    
    
def main():

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = "YOUR TOKEN!!!"
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    
    group_id = 'YOUR GROUP ID!!!'
    
    if denetleyici == True:
        updater.dispatcher.bot.send_message(chat_id=group_id, text="Bu fiyattan "+str(fiyat)+" bu kadar "+str(sayi)+" "+coin+" "+mesaj)
    if denetleyici == False:
        updater.dispatcher.bot.send_message(chat_id=group_id, text="Bu fiyattan "+str(fiyat)+" bu kadar "+str(sayi)+" "+coin+" "+mesaj+" "+str(kar_zarar)+" "+kar_zarar_mesaj+"..Toplam kar-zarar miktarı budur : "+str(toplam_kar_zarar))
    
    
    updater.stop()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    
    


if __name__ == '__main__':
    main()